import zlib
from logging import info

from flask import Flask, request
from flask_socketio import SocketIO, Namespace, emit

from openfabric_pysdk.register import OpenfabricRegister
from openfabric_pysdk.util import Util


class OpenfabricSocket(Namespace):
    __socket_io = None
    __session = None

    # def run(self, app):
    #     self.__socket_io.run(app)

    def __init__(self, socket_namespace, socket_session, app: Flask):
        super().__init__(socket_namespace)
        self.__session = socket_session
        # Set this variable to "threading", "eventlet" or "gevent" to test the
        # different async modes, or leave it set to None for the application to choose
        # the best option based on installed packages.
        async_mode = "eventlet"
        self.__socket_io = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*')
        self.__socket_io.on_namespace(self)
        self.__socket_io.run(app)

    def on_execute(self, data):
        # Uncompress data
        uncompressed = zlib.decompress(data)
        json = uncompressed.decode('utf-8')
        # Input Object
        object_clazz = Util.import_class(OpenfabricRegister.input_type)
        instance = object_clazz(json)
        result = OpenfabricRegister.execution_function(instance)
        emit('response', result)

    def on_connect(self):
        print(f'Client connected {request.sid} on {request.host}')

    def on_disconnect(self):
        print(f'Client disconnected {request.sid} on {request.host}')
