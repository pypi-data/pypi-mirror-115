from .bert2tf_pb2 import Request


def is_data_request(req: Request) -> bool:
    """check if the request is data request

    """
    req_type = type(req)
    return req_type != Request.ControlRequest


def is_idle_request(req: Request) -> bool:
    """check if the request is idle request"""
    if type(req) == Request.ControlRequest and req.command == Request.ControlRequest.Command.IDLE:
        return True
    return False


def add_envelope(req: bert2tf_pb2.Request, pod_name: str, client_id: str) -> bert2tf_pb2.Message:
    """Add envelope to a request and make it as a complete message, which can be transmitted between pods.

    :param req: the protobuf request
    :param pod_name: the name of the current pod
    :param client_id: the id of the send pod
    :return: the resulted protobuf message
    """
    msg = bert2tf_pb2.Message()
    msg.envelope.client_id = client_id
    if req.request_id is not None:
        msg.envelope.request_id = req.request_id
    else:
        raise AttributeError('"request_id" is missing or unset!')
    add_route(msg.envelope, pod_name, client_id)
    msg.request.CopyFrom(req)

    return msg


def add_route(envelope: bert2tf_pb2.Envelope, pod_name: str, identity: str):
    r = envelope.routes.add()
    r.pod = pod_name
    r.start_time.GetCurrentTime()
    r.pod_id = identity
