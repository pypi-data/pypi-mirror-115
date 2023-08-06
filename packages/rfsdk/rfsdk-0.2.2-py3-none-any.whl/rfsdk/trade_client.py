# -*- coding: utf-8 -*-
import json
import base64


try:
    from rfsdk.protocol.trade.trade_futures_pb2 import OrderInfo
    from rfsdk.protocol.trade.trade_futures_pb2 import TradeReportInfo
    # from google.protobuf import json_format
except Exception as e:
    print(u'11111 缺少依赖库，订阅推送类业务将无法正常使用')

from rfsdk.gateway import Gateway

from rfsdk.service_method import *
import rfsdk.account_req_helper as account
import rfsdk.trade_req_helper as trade

from rfsdk.comm_utils import parse_exchange_id, parse_broker_info


class BrokerType(object):
    SimNow = 'SimNow'
    SimTrade = 'SimTrade'


class PlatformType(object):
    SIMULATE = 'SIMULATE'
    CTP = 'CTP'
    UFX = 'UFX'
    KSFT = 'KSFT'


class TradeClient(object):

    def __init__(self, inter_service):
        self._investor_key = None
        self._rpc_call = None
        self._inter_service = None
        if isinstance(inter_service, Gateway):  # 暂时只支持网关接入
            self._inter_service = inter_service
            self._inter_service.set_protocol_head(chr(0x0f))
            self._rpc_call = self._inter_service.gateway_call
        else:
            raise Exception('not supported service type')

    def start(self):
        self._inter_service.connect()

    def subscribe_trade(self, func):
        self._inter_service.get_client().register_cb(TOPIC_TRADE_FUTURES,
                                                     lambda base64_msg: self._inner_cb(base64_msg, TradeReportInfo(),
                                                                                       func))
        self._inter_service.get_client().subscribe(TOPIC_TRADE_FUTURES)

    def unsubscribe_trade(self):
        self._inter_service.get_client().unsubscribe(TOPIC_TRADE_FUTURES)

    def subscribe_order(self, func):
        self._inter_service.get_client().register_cb(TOPIC_ORDER_FUTURES,
                                                     lambda base64_msg: self._inner_cb(base64_msg, OrderInfo(), func))
        self._inter_service.get_client().subscribe(TOPIC_ORDER_FUTURES)

    def unsubscribe_order(self):
        self._inter_service.get_client().unsubscribe(TOPIC_ORDER_FUTURES)

    def login(self,
              investor_id,
              trade_password,
              broker_type,
              interface_type
              ):
        trade_login_req = trade.make_login_req(investor_id=investor_id,
                                               trade_password=trade_password,
                                               op_station=None,
                                               interface_type=None,
                                               account_type=trade.AccountType.AccountType_FUTURES,
                                               broker_id=None,
                                               user_product_info=None,
                                               app_id=None,
                                               auth_code=None,
                                               collect_info=None,
                                               flow_path=None,
                                               client_public_ip=None,
                                               client_port=None,
                                               md_op_station=None,
                                               client_id=None,
                                               client_info=None,
                                               is_auto_confirm=None,
                                               is_sync_position=None,
                                               is_check_pwd=None,
                                               op_station_off=None)
        try:
            qsid, wtid = parse_broker_info(broker_type, interface_type)
        except Exception as e:
            print(e)
            return False

        req = account.make_login_req(login=trade_login_req, qsid=qsid, wtid=wtid)

        ret, rsp = self._rpc_call(SERVICE_ACCOUNT, METHOD_ACCOUNT_LOGIN, req)

        if ret == 0:
            rsp_json = json.loads(rsp)
            self._investor_key = rsp_json['login']['investor_key']
            return True
        else:
            print('login failed, msg:%s', rsp)
            return False

    def logout(self):
        if self._investor_key is None:
            return -1, 'please login first!'

        account_logout_req = account.make_logout_req(investor_key=self._investor_key)
        return self._rpc_call(SERVICE_ACCOUNT, METHOD_ACCOUNT_LOGOUT, account_logout_req)

    def query_asset(self,
                    currency_id=None,
                    biz_type=None,
                    account_id=None,
                    client_id=None,
                    trading_day=None):
        req = trade.make_query_asset_req(investor_key=self._investor_key,
                                         currency_id=currency_id,
                                         biz_type=biz_type,
                                         account_id=account_id,
                                         client_id=client_id,
                                         trading_day=trading_day)
        return self._rpc_call(SERVICE_TRADER_FUTURES, METHOD_TRADER_QUERY_ASSET, req)

    def query_order(self,
                    instrument_id=None,
                    exchange_id=None,
                    order_sys_id=None,
                    insert_time_start=None,
                    insert_time_end=None,
                    client_id=None):
        if instrument_id is not None:
            exchange_id = parse_exchange_id(instrument_id)

        req = trade.make_query_order_req(investor_key=self._investor_key,
                                         instrument_id=instrument_id,
                                         exchange_id=exchange_id,
                                         order_sys_id=order_sys_id,
                                         insert_time_start=insert_time_start,
                                         insert_time_end=insert_time_end,
                                         client_id=client_id)
        return self._rpc_call(SERVICE_TRADER_FUTURES, METHOD_TRADER_QUERY_ORDER, req)

    def query_position_detail(self,
                              instrument_id=None,
                              exchange_id=None,
                              historical_date=None,
                              type=None):
        req = trade.make_query_position_detail_req(investor_key=self._investor_key,
                                                   instrument_id=instrument_id,
                                                   exchange_id=exchange_id,
                                                   historical_date=historical_date,
                                                   type=type)
        return self._rpc_call(SERVICE_TRADER_FUTURES, METHOD_TRADER_QUERY_POSITION_DETAIL, req)

    def order_insert(self, instrument_id,
                     direction,
                     comb_offset_flag,
                     volume_total_original,
                     order_no=None,
                     order_price_type=trade.OrderPriceType.OrderPriceType_LimitPrice,
                     limit_price=None,  # 根据order_price_type类型填写
                     comb_hedge_flag='0',  # 投机
                     time_condition=trade.TimeConditionType.TimeConditionType_GFD,
                     gtd_date=None,
                     volume_condition=None,
                     min_volume=None,
                     contingent_condition=None,
                     stop_price=None,
                     force_close_reason=None,
                     user_force_close=None,
                     is_swap_order=None,
                     local_order_no=None,
                     client_id=None,
                     source=None,
                     is_back_hand=None,
                     is_change_order=None,
                     new_order_price_type=None,
                     new_limit_price=None,
                     price_tick_num=None):
        exchange_id = parse_exchange_id(instrument_id)
        if order_price_type is trade.OrderPriceType.OrderPriceType_LimitPrice and limit_price is None:
            return -1, u'价格类型为限价，请填写价格'

        req = trade.make_order_insert_req(investor_key=self._investor_key,
                                          instrument_id=instrument_id,
                                          order_no=order_no,
                                          order_price_type=order_price_type,
                                          direction=direction,
                                          comb_offset_flag=comb_offset_flag,
                                          comb_hedge_flag=comb_hedge_flag,
                                          limit_price=limit_price,
                                          volume_total_original=volume_total_original,
                                          time_condition=time_condition,
                                          gtd_date=gtd_date,
                                          volume_condition=volume_condition,
                                          min_volume=min_volume,
                                          contingent_condition=contingent_condition,
                                          stop_price=stop_price,
                                          force_close_reason=force_close_reason,
                                          user_force_close=user_force_close,
                                          is_swap_order=is_swap_order,
                                          exchange_id=exchange_id,
                                          local_order_no=local_order_no,
                                          client_id=client_id,
                                          source=source,
                                          is_back_hand=is_back_hand,
                                          is_change_order=is_change_order,
                                          new_order_price_type=new_order_price_type,
                                          new_limit_price=new_limit_price,
                                          price_tick_num=price_tick_num)
        return self._rpc_call(SERVICE_TRADER_FUTURES, METHOD_TRADER_INSERT_ORDER, req)

    def order_cancel(self,
                     order_no,
                     cancel_order_no=None,
                     order_sys_id=None,
                     instrument_id=None,
                     investor_id=None,
                     client_id=None,
                     is_change_order=None,
                     volume_total_original=None,
                     order_price_type=None,
                     limit_price=None,
                     price_tick_num=None):
        exchange_id = parse_exchange_id(instrument_id)
        req = trade.make_order_cancel_req(investor_key=self._investor_key,
                                          cancel_order_no=cancel_order_no,
                                          order_no=order_no,
                                          exchange_id=exchange_id,
                                          order_sys_id=order_sys_id,
                                          instrument_id=instrument_id,
                                          investor_id=investor_id,
                                          client_id=client_id,
                                          is_change_order=is_change_order,
                                          volume_total_original=volume_total_original,
                                          order_price_type=order_price_type,
                                          limit_price=limit_price,
                                          price_tick_num=price_tick_num)
        return self._rpc_call(SERVICE_TRADER_FUTURES, METHOD_TRADER_CANCEL_ORDER, req)

    def query_instrument(self,
                         instrument_id=None):
        exchange_id = parse_exchange_id(instrument_id)
        req = trade.make_query_instrument_req(investor_key=self._investor_key,
                                              exchange_id=exchange_id,
                                              instrument_id=instrument_id)
        return self._rpc_call(SERVICE_TRADER_FUTURES, METHOD_TRADER_QUERY_INSTRUMENT, req)

    def _inner_cb(self, base64_msg, msg_obj, func):
        msg_bytes = base64.decodebytes(bytes(base64_msg, encoding='utf-8'))

        msg_obj.ParseFromString(msg_bytes)
        msg = json_format.MessageToJson(msg_obj, preserving_proto_field_name=True)
        func(msg)
