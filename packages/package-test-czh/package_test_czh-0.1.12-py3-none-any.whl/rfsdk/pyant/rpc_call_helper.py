import json

try:
    from google.protobuf import json_format
    SUPPORT_PY_PROTOBUF = True
except Exception as e:
    SUPPORT_PY_PROTOBUF = False

from ant_rpc import json_call_wait
from ant_rpc import Endpoint
from ant_rpc import Option


def rpc_call(service_name, method, data, op=Option.default_instance(), ep=Endpoint.default_instance()):

    if isinstance(data, str):
        msg_json = data
    elif isinstance(data, dict):
        msg_json = json.dumps(data)
    elif SUPPORT_PY_PROTOBUF and isinstance(data, google.protobuf.message.Message):
        msg_json = json_format.MessageToJson(
            data, preserving_proto_field_name=True)
    else:
        return -1, 'not supported data type'

    ret, msg = json_call_wait(service_name, method, msg_json, op, ep)
    return ret, msg


def async_rpc_call(cb_func, service_name, method, data, op=None, ep=None):
    pass
