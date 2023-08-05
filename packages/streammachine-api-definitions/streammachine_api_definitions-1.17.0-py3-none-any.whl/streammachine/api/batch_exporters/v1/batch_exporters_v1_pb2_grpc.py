# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from streammachine.api.batch_exporters.v1 import batch_exporters_v1_pb2 as streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2


class BatchExportersServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListBatchExporters = channel.unary_unary(
                '/streammachine.api.batch_exporters.v1.BatchExportersService/ListBatchExporters',
                request_serializer=streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.ListBatchExportersRequest.SerializeToString,
                response_deserializer=streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.ListBatchExportersResponse.FromString,
                )
        self.GetBatchExporter = channel.unary_unary(
                '/streammachine.api.batch_exporters.v1.BatchExportersService/GetBatchExporter',
                request_serializer=streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.GetBatchExporterRequest.SerializeToString,
                response_deserializer=streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.GetBatchExporterResponse.FromString,
                )
        self.DeleteBatchExporter = channel.unary_unary(
                '/streammachine.api.batch_exporters.v1.BatchExportersService/DeleteBatchExporter',
                request_serializer=streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.DeleteBatchExporterRequest.SerializeToString,
                response_deserializer=streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.DeleteBatchExporterResponse.FromString,
                )
        self.CreateBatchExporter = channel.unary_unary(
                '/streammachine.api.batch_exporters.v1.BatchExportersService/CreateBatchExporter',
                request_serializer=streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.CreateBatchExporterRequest.SerializeToString,
                response_deserializer=streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.CreateBatchExporterResponse.FromString,
                )


class BatchExportersServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ListBatchExporters(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBatchExporter(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteBatchExporter(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateBatchExporter(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BatchExportersServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListBatchExporters': grpc.unary_unary_rpc_method_handler(
                    servicer.ListBatchExporters,
                    request_deserializer=streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.ListBatchExportersRequest.FromString,
                    response_serializer=streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.ListBatchExportersResponse.SerializeToString,
            ),
            'GetBatchExporter': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBatchExporter,
                    request_deserializer=streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.GetBatchExporterRequest.FromString,
                    response_serializer=streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.GetBatchExporterResponse.SerializeToString,
            ),
            'DeleteBatchExporter': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteBatchExporter,
                    request_deserializer=streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.DeleteBatchExporterRequest.FromString,
                    response_serializer=streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.DeleteBatchExporterResponse.SerializeToString,
            ),
            'CreateBatchExporter': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateBatchExporter,
                    request_deserializer=streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.CreateBatchExporterRequest.FromString,
                    response_serializer=streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.CreateBatchExporterResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'streammachine.api.batch_exporters.v1.BatchExportersService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class BatchExportersService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListBatchExporters(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/streammachine.api.batch_exporters.v1.BatchExportersService/ListBatchExporters',
            streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.ListBatchExportersRequest.SerializeToString,
            streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.ListBatchExportersResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBatchExporter(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/streammachine.api.batch_exporters.v1.BatchExportersService/GetBatchExporter',
            streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.GetBatchExporterRequest.SerializeToString,
            streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.GetBatchExporterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteBatchExporter(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/streammachine.api.batch_exporters.v1.BatchExportersService/DeleteBatchExporter',
            streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.DeleteBatchExporterRequest.SerializeToString,
            streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.DeleteBatchExporterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateBatchExporter(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/streammachine.api.batch_exporters.v1.BatchExportersService/CreateBatchExporter',
            streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.CreateBatchExporterRequest.SerializeToString,
            streammachine_dot_api_dot_batch__exporters_dot_v1_dot_batch__exporters__v1__pb2.CreateBatchExporterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
