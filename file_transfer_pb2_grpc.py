# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import file_transfer_pb2 as file__transfer__pb2


class FileTransferStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendFile = channel.stream_unary(
                '/filetransfer.FileTransfer/SendFile',
                request_serializer=file__transfer__pb2.Chunk.SerializeToString,
                response_deserializer=file__transfer__pb2.Response.FromString,
                )


class FileTransferServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendFile(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FileTransferServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendFile': grpc.stream_unary_rpc_method_handler(
                    servicer.SendFile,
                    request_deserializer=file__transfer__pb2.Chunk.FromString,
                    response_serializer=file__transfer__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'filetransfer.FileTransfer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FileTransfer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendFile(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/filetransfer.FileTransfer/SendFile',
            file__transfer__pb2.Chunk.SerializeToString,
            file__transfer__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
