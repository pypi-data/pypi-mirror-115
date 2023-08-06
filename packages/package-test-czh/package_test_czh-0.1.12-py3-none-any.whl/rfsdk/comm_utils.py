# -*- coding: utf-8 -*-
import os
import inspect
import re
import json

with open(os.path.join(os.path.dirname(__file__), 'instrument.json'), 'r') as f:
    _instrument_list = json.load(f)

with open(os.path.join(os.path.dirname(__file__), 'station.json'), 'r') as f:
    _station_list = json.load(f)


def generate_req(frame):
    args, _, _, values = inspect.getargvalues(frame)
    req = dict()
    for arg_name in args:
        value = values[arg_name]
        if value is not None:
            req[arg_name] = value

    return req


def parse_exchange_id(instrument_id):
    ret = re.findall(r'^[a-zA-Z]+', instrument_id)
    instrument_code = ret[0].lower()
    for item in _instrument_list:
        # print(item)
        if instrument_code in _instrument_list[item]:
            return item
    else:
        raise Exception(u'非法的合约品种')


def parse_broker_info(broker_type, interface_type):
    if broker_type in _station_list and interface_type in _station_list[broker_type]['wt_info']:
        return _station_list[broker_type]['qsid'], _station_list[broker_type]['wt_info'][interface_type]
    else:
        raise Exception(u'请选择支持的期商及柜台')


if __name__ == '__main__':
    print(parse_exchange_id('ag2110'))
    print(parse_broker_info('SimNow', 'CTP'))
