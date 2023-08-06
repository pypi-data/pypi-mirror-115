# -*- coding: utf-8 -*-
import json
from threading import Thread
from time import sleep

from ant_rpc import GatewayAuthenticator
from ant_rpc import Endpoint
from ant_rpc import Option
from ant_rpc import CommunicationType
from ant_rpc import ProtocolType
from ant_rpc import Client
from ant_rpc import Server
from ant_rpc import init_gateway_auth
from rpc_call_helper import rpc_call

from rfsdk.service_method import *


class Gateway(object):

    def __init__(self, ip, port, config_path):
        self._ip = ip
        self._port = port
        self._config_path = config_path
        self._client = None
        self._server = None
        self._option = Option()
        self._protocol_head = None
        self._service_name = SERVICE_GATEWAY
        self._use_verbose_log = True

    def set_protocol_head(self, protocol_head):
        self._protocol_head = protocol_head

    def set_default_service_name(self, service_name):
        self._service_name = service_name

    def set_verbose_log(self, need_log):
        self._use_verbose_log = need_log

    def connect(self):
        t = Thread(target=self._connect_gateway_with_auth)
        t.start()
        sleep(1)

    def _connect_gateway_with_auth(self):
        gateway_auth = GatewayAuthenticator()
        init_gateway_auth(gateway_auth, self._ip)

        self._client = Client(name=self._service_name, need_ns=False, auth=gateway_auth)
        # self._client.set_used_verbose_log(self._use_verbose_log)
        ep = Endpoint()
        ep.set_communication_type(CommunicationType.kCommunicationTcp)
        ep.set_ip(self._ip)
        ep.set_port(self._port)
        ep.set_protocol(ProtocolType.kProtocolGateway)
        ep.set_required_auth(True)

        self._client.append_endpoint(ep)

        self._client.set_on_create_channel(
            lambda conn: conn.get_codec().set_protocol_head(self._protocol_head))

        if self._server is None :
            self._server = Server('client_gateway')
            self._server.start(self._config_path)

        self._server.add_client(self._client)

        if self._client.sync_auth():
            pass
        else:
            print('gateway auth failed!')
            return

    def get_server(self):
        return self._server

    def get_client(self):
        return self._client

    def gateway_call(self, service, method, req):
        self._option.set_forward_service_name(service)
        ret, rsp = rpc_call(self._service_name, method, req, self._option)
        if method is METHOD_ACCOUNT_LOGIN and ret == 0:
            rsp_json = json.loads(rsp)
            investor_key = str(rsp_json['login']['investor_key'])
            channel_key = investor_key[0:-2]
            interface_type = int(investor_key[1:3])
            service_type = 2 ** interface_type
            self._option.set_channel_key(channel_key)
            self._option.set_service_type(service_type)

        return ret, rsp
