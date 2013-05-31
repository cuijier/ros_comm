import zmq
from rosmaster.genpythrift.MasterAPI import MasterAPI
from rosmaster import TZmqServer

try:
    import _thread
except ImportError:
    import thread as _thread


class WrappedHandler(MasterAPI.Iface):

    def __init__(self, handler):
        self.handler = handler

    def getParamNames(self, caller_id):
        result = self.handler.getParamNames(caller_id)
        return [str(i) for i in result]

    def getUri(self, caller_id):
        result = self.handler.getUri(caller_id)
        return [str(i) for i in result]

    def getPid(self, caller_id):
        result = self.handler.getPid(caller_id)
        return [str(i) for i in result]

    def getSystemState(self, caller_id):
        result = self.handler.getSystemState(caller_id)
        return [str(i) for i in result]

    def lookupService(self, caller_id, service_):
        result = self.handler.lookupService(caller_id, service_)
        return [str(i) for i in result]

    def registerService(self, caller_id, service_, service_api, caller_api):
        result = self.handler.registerService(caller_id, service_, service_api,
            caller_api)
        return [str(i) for i in result]



class ZeroMQNode(object):
    def __init__(self, port, handler):
        self.port = port
        self.handler = WrappedHandler(handler)
        self.processor = MasterAPI.Processor(self.handler)

        self.ctx = zmq.Context()
        self.reqrep_server = TZmqServer.TZmqServer(self.processor, self.ctx,
            'tcp://0.0.0.0:%d' % self.port, zmq.REP)
        self.multiserver = TZmqServer.TZmqMultiServer()
        self.multiserver.servers.append(self.reqrep_server)

    def start(self):
        self.uri = 'tcp://0.0.0.0:%d' % self.port
        _thread.start_new_thread(self.multiserver.serveForever, ())
