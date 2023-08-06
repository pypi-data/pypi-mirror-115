# -*- coding: utf-8 -*-
import base64

try:
    from rfsdk.protocol.trade.trade_futures_pb2 import OrderInfo
    from rfsdk.protocol.trade.trade_futures_pb2 import TradeReportInfo
    from rfsdk.protocol.quote.quote_pb2 import NotificationTick
    from google.protobuf import json_format
except Exception as e:
    print(u'缺少依赖库，订阅推送类业务将无法正常使用')

from rfsdk.gateway import Gateway

from rfsdk.service_method import *
import rfsdk.account_req_helper as account
import rfsdk.trade_req_helper as trade
import rfsdk.quote_req_helper as quote

from rfsdk.comm_utils import parse_exchange_id, parse_broker_info

class QuoteClient(object):

    def __init__(self, inter_service):
        self._investor_key = None
        self._rpc_call = None
        self._inter_service = None
        if isinstance(inter_service, Gateway):  # 暂时只支持网关接入
            self._inter_service = inter_service
            self._inter_service.set_default_service_name(SERVICE_MARKETDATA)
            self._inter_service.set_protocol_head(chr(0x0c))
            #self._inter_service.set_verbose_log(False)
            self._rpc_call = self._inter_service.gateway_call
        else:
            raise Exception('not supported service type')

    def start(self):
        self._inter_service.connect()

    def query_instrument(self,
                         instrument_id=None):
        exchange_id = parse_exchange_id(instrument_id)
        req = trade.make_query_instrument_req(investor_key=self._investor_key,
                                              exchange_id=exchange_id,
                                              instrument_id=instrument_id)
        return self._rpc_call(SERVICE_TRADER_FUTURES, METHOD_TRADER_QUERY_INSTRUMENT, req)

    def query_last_quote(self,
                         instrument_id,
                         instrument_type=quote.InstrumentType.InstrumentType_Future):
        exchange_id = parse_exchange_id(instrument_id)
        req = quote.make_query_last_quote_req(exchange_id=exchange_id, instrument_id=instrument_id,
                                              instrument_type=instrument_type)
        return self._rpc_call(SERVICE_QUOTA, METHOD_MD_QUERY_LAST_QUOTE, req)

    def subscribe_quote(self, func, instrument_id):
        self._inter_service.get_client().register_cb(TOPIC_QUOTE_TICK_FUTURES + '.' + instrument_id,
                                                     lambda base64_msg: self._inner_cb(base64_msg, NotificationTick(),
                                                                                       func))
        self._inter_service.get_client().subscribe(TOPIC_QUOTE_TICK_FUTURES + '.' + instrument_id)

    def unsubscribe_quote(self, instrument_id):
        self._inter_service.get_client().unsubscribe(TOPIC_QUOTE_TICK_FUTURES + '.' + instrument_id)

    def _inner_cb(self, base64_msg, msg_obj, func):
        msg_bytes = base64.decodebytes(bytes(base64_msg, encoding='utf-8'))

        msg_obj.ParseFromString(msg_bytes)
        msg = json_format.MessageToJson(msg_obj, preserving_proto_field_name=True)
        func(msg)
