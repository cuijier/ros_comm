import zmq
from thrift.contrib.zeromq import TZmqServer
from rosmaster.thrift import MasterAPI

try:
    import _thread
except ImportError:
    import thread as _thread


class StorageHandler(storage.Storage.Iface):
  def __init__(self):
    self.value = 0

  def incr(self, amount):
    self.value += amount

  def get(self):
    return self.value


class ZeroMQNode(object):
    def __init__(self, port, handler):
        self.handler = handler
        self.processor = MasterAPI.MasterAPI.Processor(self.handler)

        self.ctx = zmq.Context()
        self.reqrep_server = TZmqServer.TZmqServer(self.processor, self.ctx,
            "tcp://0.0.0.0:%d" % self.port, zmq.REP)
        self.multiserver = TZmqServer.TZmqMultiServer()
        self.multiserver.servers.append(self.reqrep_server)

    def start(self):
        _thread.start_new_thread(self.multiserver.serveForever, ())
