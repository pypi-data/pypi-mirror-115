# -*- coding: utf-8 -*-
import json
import os
import sys
from time import sleep

pyfst_root_path = os.path.dirname(os.path.dirname(__file__))  # 修改为pyfst目录

pyant_path = os.path.join(pyfst_root_path, 'pyant')
if pyant_path not in sys.path:
    sys.path.append(pyant_path)

protocol_path = os.path.join(pyfst_root_path, 'protocol')
if protocol_path not in sys.path:
    sys.path.append(protocol_path)

from gateway import Gateway
from trade_client import TradeClient, BrokerType, PlatformType
from trade_req_helper import ActionType


def trade_api_test():
    client = TradeClient(Gateway('172.19.80.16', 5050, 'rpc.ini'))  # 172.19.80.16:5050 为网关地址，rpc.ini为服务配置文件，会随包发布（一般无需修改）
    client.start() # 启动服务，接入交易网关

    if not client.login(investor_id='xxx', trade_password='xxx', broker_type=BrokerType.SimNow,
                        interface_type=PlatformType.CTP):
        # login failed
        return

    # 订阅委托回报
    client.subscribe_order(lambda msg: print('order cb, msg:\n%s\n' % msg))

    # 订阅成交回报
    client.subscribe_trade(lambda msg: print('trade cb, msg:\n%s\n' % msg))

    # 查询资产
    ret, rsp = client.query_asset()
    print('query_assert rsp:\n%s\n' % rsp)

    sleep(1)  # CTP有流控，加点延时避免查询失败
    # 查询持仓明细
    ret, rsp = client.query_position_detail()
    print('query_position_detail rsp:\n%s\n' % rsp)

    sleep(1)
    # 查询合约
    ret, rsp = client.query_instrument(instrument_id='ag2110')
    print('query_instrument rsp:\n%s\n' % rsp)

    # 报单录入，'5000'价格'买入'合约'ag2110',买入数量为'100'
    # Notes:为了测试撤单，价格小于测试时的市价
    ret, rsp = client.order_insert(instrument_id='ag2110', comb_offset_flag='0',
                                   direction=ActionType.ActionType_BUY, limit_price=5000, volume_total_original=100)
    print('order_insert rsp:\n%s\n' % rsp)
    if 0 == ret:
        rsp_json = json.loads(rsp)
        order_no = rsp_json['order']['order_no']

        # 查询报单
        ret, rsp = client.query_order()  # 填写instrument_id参数可查指定合约报单
        print('query_order rsp:\n%s\n' % rsp)

        sleep(5)

        # 撤单
        ret, rsp = client.order_cancel(instrument_id='ag2110', order_no=order_no)
        print('order_cancel rsp:\n%s\n' % rsp)


if __name__ == '__main__':
    trade_api_test()
