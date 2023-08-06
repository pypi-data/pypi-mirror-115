import asyncio
import datetime
import decimal
import traceback
import uuid
import warnings
from dataclasses import dataclass
from functools import partial
from logging import LoggerAdapter
from typing import Dict, List, Any, Callable, Union

import aiohttp
import simplejson as json
from aio_pika import connect_robust, IncomingMessage, Exchange, Message, DeliveryMode
from envparse import env
from vtb_http_interaction.keycloak_gateway import KeycloakConfig
from vtb_http_interaction.services import AuthorizationHttpService

from state_service_utils.enums_client import enums
from .exceptions import StateServiceException
from .logging import create_logger

DEBUG = env.bool("DEBUG", default=False)
STATE_SERVICE_URL = env.str("STATE_SERVICE_URL", default=None)
STATE_SERVICE_TOKEN = env.str('STATE_SERVICE_TOKEN', default=None)
STATE_SERVICE_MOCK = env.bool('STATE_SERVICE_MOCK', default=False)

KEY_CLOAK_SERVER_URL = env.str("KEY_CLOAK_SERVER_URL", default=None)
KEY_CLOAK_REALM_NAME = env.str("KEY_CLOAK_REALM_NAME", default=None)
KEY_CLOAK_CLIENT_ID = env.str("KEY_CLOAK_CLIENT_ID", default=None)
KEY_CLOAK_CLIENT_SECRET_KEY = env.str("KEY_CLOAK_CLIENT_SECRET_KEY", default=None)
REDIS_CONNECTION_STRING = env.str("REDIS_CONNECTION_STRING", default=None)

KEY_CLOAK_CONFIG = None
if REDIS_CONNECTION_STRING and KEY_CLOAK_SERVER_URL and \
        KEY_CLOAK_REALM_NAME and KEY_CLOAK_CLIENT_ID and KEY_CLOAK_CLIENT_SECRET_KEY:
    KEY_CLOAK_CONFIG = KeycloakConfig(
        server_url=KEY_CLOAK_SERVER_URL,
        client_id=KEY_CLOAK_CLIENT_ID,
        realm_name=KEY_CLOAK_REALM_NAME,
        client_secret_key=KEY_CLOAK_CLIENT_SECRET_KEY
    )

LOG_FULL = 'full'
LOG_SHORT = 'short'


if not DEBUG and not (STATE_SERVICE_MOCK or STATE_SERVICE_TOKEN or KEY_CLOAK_CONFIG):
    raise EnvironmentError(
        '`STATE_SERVICE_TOKEN` or `KEY_CLOAK_CONFIG` is required when you`re not using `STATE_SERVICE_MOCK` or debug.')

if STATE_SERVICE_TOKEN:
    # TODO: Удалить класс в версии 2.0.0
    warnings.warn(
        'Поддержка переменной окружение STATE_SERVICE_TOKEN будет удалена в версии 1.7.0. \
Настройте интеграцию с keycloak, указав REDIS_CONNECTION_STRING, KEY_CLOAK_SERVER_URL, \
KEY_CLOAK_REALM_NAME, KEY_CLOAK_CLIENT_ID и KEY_CLOAK_CLIENT_SECRET_KEY.',
        DeprecationWarning, stacklevel=2)


@dataclass
class OrderAction:
    order_id: str
    action_id: str
    graph_id: str


async def add_action_event(*, action: OrderAction, type, subtype, status='', data=None, log_level=LOG_FULL):
    if not log_level:
        return

    request_data = {
        'type': type,
        'subtype': subtype,
        'status': status,
    }
    if log_level == LOG_FULL:
        request_data['data'] = data

    request_data.update(action.__dict__)
    await _make_request(
        url=f'{STATE_SERVICE_URL}/actions/',
        data=request_data
    )


async def add_event(*, action: OrderAction, item_id: str,
                    type, subtype, status='', data=None):
    """ Создание события в сервисе состояний """
    data = {
        'item_id': item_id,
        'type': type,
        'subtype': subtype,
        'status': status,
        'data': data
    }
    data.update(action.__dict__)
    await _make_request(
        url=f'{STATE_SERVICE_URL}/events/',
        data=data
    )


async def add_events(*, action: OrderAction, events: List[Dict]) -> Any:
    """ Создание списка событий в сервисе состояний одним запросом """
    data = {
        'events': events
    }
    data.update(action.__dict__)
    return await _make_request(
        url=f'{STATE_SERVICE_URL}/events/bulk-add-event/',
        data=data
    )


def state_action_decorator(arg: Union[bool, Callable] = True):
    def func_decorator(func):
        async def wrapper(*, order_action: OrderAction, node, action_type=enums.ActionDeploy.RUN_NODE.value, task_logger,
                          log_level=LOG_FULL, **kwargs):
            node_name = node if isinstance(node, str) else node.path
            await add_action_event(
                action=order_action,
                type=enums.ActionType.DEPLOY.value,
                subtype=action_type,
                status='%s:%s' % (node_name, enums.ActionStatus.STARTED.value),
                data=kwargs,
                log_level=log_level
            )
            try:
                if action_type not in enums.ActionDeploy._value2member_map_.keys():
                    raise StateServiceException(f'Invalid action type: {action_type}')
                if additional_call_kwargs:
                    kwargs.update({
                        'order_action': order_action,
                        'action_type': action_type,
                        'task_logger': task_logger
                    })
                result = await func(
                    node=node,
                    **kwargs,
                )
                status = '%s:%s' % (node_name, enums.ActionStatus.COMPLETED.value)
            except Exception as e:
                tb = traceback.format_exc()
                result = {
                    'error': str(e),
                    'traceback': tb}
                status = '%s:%s' % (node_name, enums.ActionStatus.ERROR.value)
                task_logger.error(
                    f"Error in action ({status}): {tb}")
                log_level = LOG_FULL
            await add_action_event(
                action=order_action,
                type=enums.ActionType.DEPLOY.value,
                subtype=action_type,
                status=status,
                data=result,
                log_level=log_level
            )
            return result
        return wrapper
    if callable(arg):
        # it means that the decorator was called without its arguments, therefore we
        # are passing argument further to the func_decorator and assigning default argument value
        additional_call_kwargs = True
        return func_decorator(arg)
    else:
        # the decorator was called with arguments, hence we are assigning the passed value to the corresponding
        # variable
        additional_call_kwargs = arg
        return func_decorator


class EventsReceiver:
    def __init__(self, fn, mq_addr, mq_input_queue, logger_name: str = ''):
        self.mq_addr = mq_addr
        self.input_queue = mq_input_queue
        self.fn = state_action_decorator()(fn)
        self.logger = create_logger(logger_name)

    async def on_message(self, message: IncomingMessage, exchange: Exchange):

        with message.process():
            data = json.loads(message.body)

            if not isinstance(data, dict):
                raise StateServiceException('Invalid message (need struct): %s', data)

            order_action = OrderAction(
                order_id=data.pop('_order_id'),
                action_id=data.pop('_action_id'),
                graph_id=data.pop('_graph_id'))
            node = data['_name']
            action_type = data.get('_type')

            task_logger = LoggerAdapter(self.logger, extra={
                'order_action': order_action.__dict__,
                'node': node,
                'action_type': action_type,
                'orchestrator_id': data.get('_id')
            })

            response = await self.fn(
                order_action=order_action,
                node=node,
                action_type=action_type,
                task_logger=task_logger,
                **data,
            )

            if not isinstance(response, str):
                response = json.dumps(response, default=default_encoder)

            await exchange.publish(
                Message(body=response.encode(), content_type="application/json",
                        correlation_id=message.correlation_id, delivery_mode=DeliveryMode.PERSISTENT),
                routing_key=message.reply_to,
            )

    async def _receive(self, loop, addr, queue_name, queue_kwargs, prefetch_count=None):
        connection = await connect_robust(addr, loop=loop)
        channel = await connection.channel()
        if prefetch_count:
            await channel.set_qos(prefetch_count=prefetch_count)
        queue = await channel.declare_queue(queue_name, **(queue_kwargs or {}), durable=True)
        await queue.consume(partial(self.on_message, exchange=channel.default_exchange))

    def run(self, queue_kwargs: dict = None, prefetch_count: int = None):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self._receive(
            loop, addr=self.mq_addr, queue_name=self.input_queue,
            queue_kwargs=queue_kwargs,
            prefetch_count=prefetch_count
        ))
        loop.run_until_complete(task)
        self.logger.info('Awaiting events')
        try:
            loop.run_forever()
        except (SystemExit, KeyboardInterrupt):
            self.logger.info('Sever stopped')


def items_from_events(events, serializer=None):
    items = {}

    # ASC to DESC
    events_for_source = events.copy()
    events_for_source.reverse()
    for event in events_for_source:
        if not serializer:
            # event is dict
            if (item_id := str(event['item_id'])) not in items:
                items[item_id] = event
        else:
            if (item_id := str(event.item_id)) not in items:
                items[item_id] = serializer(instance=event).data

    for event in events:
        if serializer:
            # we can use separate serializer, but it's overhead
            item_id = str(event.item_id)
            key = event.subtype
            status = event.status
            data = event.data
        else:
            item_id = event['item_id']
            key = event['subtype']
            status = event.pop('status', None)
            data = event.pop('data', None)
        if status and data:
            # items[item_id][f'{key}_status'] = status
            # items[item_id][f'{key}_data'] = data
            raise Exception(f'Event has both keys: status & data')
        else:
            items[item_id][key] = status or data

    return list(items.values())


def default_encoder(obj):
    """ Default JSON encoder """
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()

    if isinstance(obj, (uuid.UUID, decimal.Decimal)):
        return str(obj)

    return obj


async def _make_request(url, data: dict) -> Any:
    if STATE_SERVICE_MOCK:
        return

    if STATE_SERVICE_TOKEN:
        await _make_create_with_drf_token(url, data)
        return
    elif KEY_CLOAK_CONFIG:
        return await _make_create_with_key_cloak_token(url, data)


async def _make_create_with_drf_token(url, data: dict):
    async with aiohttp.ClientSession(headers={'Authorization': f'Token {STATE_SERVICE_TOKEN}'}) as session:
        async with session.post(url, json=data, ssl=False) as response:

            if response.status == 400:
                response_json = await response.json()
                raise StateServiceException(response_json)
            elif response.status != 201:
                response_text = await response.text()
                raise StateServiceException(f'State service request error ({response.status}): {response_text}')


async def _make_create_with_key_cloak_token(url, data: dict) -> Any:
    service = AuthorizationHttpService(KEY_CLOAK_CONFIG, REDIS_CONNECTION_STRING)

    request = {
        'method': "POST",
        'url': url,
        'cfg': {
            'json': data
        }
    }
    status, response = await service.send_request(**request)

    if status == 400:
        raise StateServiceException(response)
    elif status != 201:
        raise StateServiceException(f'State service request error ({status}): {response}')

    return response
