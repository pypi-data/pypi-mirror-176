import json
import socket
from dataclasses import dataclass
import traceback
import requests
from IPython import get_ipython
from IPython.core.ultratb import AutoFormattedTB

from streaminglogs import StreamingLogsServiceContext, ActivityLog, ExceptionLog


@dataclass
class LoggingHandler:

    __context: StreamingLogsServiceContext
    __is_debug: bool
    __origin: str
    __ip_address: str

    @classmethod
    def __init__(cls, context: StreamingLogsServiceContext, is_debug, enable_unhandled_exceptions_tracing=False):
        cls.__context = context
        cls.__is_debug = is_debug
        cls.__origin = cls.__context.origin + '.debug' if cls.__is_debug else cls.__context.origin
        cls.__ip_address = cls.__get_ip()
        if enable_unhandled_exceptions_tracing:
            get_ipython().set_custom_exc((Exception,), cls.trace_unhandled_exception)

    @classmethod
    def trace_unhandled_exception(cls, shell, etype, evalue, tb, tb_offset=None):
        shell.showtraceback((etype, evalue, tb), tb_offset=tb_offset)

        itb = AutoFormattedTB(mode='Plain', tb_offset=1)
        stb = itb.structured_traceback(etype, evalue, tb)
        sstb = itb.stb2text(stb)

        cls.trace_exception(Exception(sstb))

    @classmethod
    def trace_activity(cls, message: str, tags=None, console_only: bool = False):
        if tags is None:
            tags = []

        if cls.__is_debug:
            print(message)

        activity_log = ActivityLog(cls.__origin, message, cls.__ip_address, None, [] if tags is None else tags)
        message = {
            'payload': activity_log.as_legacy_dict(),
            'routingKey': cls.__build_routing_key(activity_log.origin, activity_log.input_type, console_only, tags)
        }
        response = requests.post(
            cls.__context.endpoint,
            data=json.dumps(message, indent=4, sort_keys=True, default=str),
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code != 200:
            # raise NameError('Streaming Logs API Error {}'.format(response.content.decode('utf-8')))
            print('Streaming Logs API Error {}'.format(response.content.decode('utf-8')))

    @classmethod
    def trace_exception(cls, ex: Exception, tags=None, console_only: bool = False):
        if tags is None:
            tags = []

        if cls.__is_debug:
            print(ex)

        stacktrace = ''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))
        ex_log = ExceptionLog(cls.__origin, None, stacktrace, ex, None, cls.__ip_address, None, [] if tags is None else tags)
        message = {
            'payload': ex_log.as_legacy_dict(),
            'routingKey': cls.__build_routing_key(ex_log.origin, ex_log.input_type, console_only, tags)
        }
        response = requests.post(
            cls.__context.endpoint,
            data=json.dumps(message, indent=4, sort_keys=True, default=str),
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code != 200:
            # raise NameError('Streaming Logs API Error {}'.format(response.content.decode('utf-8')))
            print('Streaming Logs API Error {}'.format(response.content.decode('utf-8')))

    @staticmethod
    def __build_routing_key(origin, input_type, console_only: bool, tags: [str]):
        if tags is not None:
            return '{}.{}.{}.{}'.format('ConsoleOnly' if console_only else 'Storable', origin, input_type, '.'.join(tags))
        return '{}.{}.{}'.format('ConsoleOnly' if console_only else 'Storable', origin, input_type)

    @staticmethod
    def __get_ip():
        return '0.0.0.0'
        # This cause problems on some environments like for example Airflow
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            ip_address = s.getsockname()[0]
        except Exception as ex:
            print(ex)
            ip_address = '127.0.0.1'
        finally:
            s.close()
        return ip_address
