# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from streammachine.api.kafka_exporters.v1 import kafka_exporters_v1_pb2 as streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2


class KafkaExportersServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListKafkaExporters = channel.unary_unary(
                '/streammachine.api.kafka_exporters.v1.KafkaExportersService/ListKafkaExporters',
                request_serializer=streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.ListKafkaExportersRequest.SerializeToString,
                response_deserializer=streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.ListKafkaExportersResponse.FromString,
                )
        self.GetKafkaExporter = channel.unary_unary(
                '/streammachine.api.kafka_exporters.v1.KafkaExportersService/GetKafkaExporter',
                request_serializer=streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.GetKafkaExporterRequest.SerializeToString,
                response_deserializer=streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.GetKafkaExporterResponse.FromString,
                )
        self.DeleteKafkaExporter = channel.unary_unary(
                '/streammachine.api.kafka_exporters.v1.KafkaExportersService/DeleteKafkaExporter',
                request_serializer=streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.DeleteKafkaExporterRequest.SerializeToString,
                response_deserializer=streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.DeleteKafkaExporterResponse.FromString,
                )
        self.CreateKafkaExporter = channel.unary_unary(
                '/streammachine.api.kafka_exporters.v1.KafkaExportersService/CreateKafkaExporter',
                request_serializer=streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.CreateKafkaExporterRequest.SerializeToString,
                response_deserializer=streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.CreateKafkaExporterResponse.FromString,
                )


class KafkaExportersServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ListKafkaExporters(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetKafkaExporter(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteKafkaExporter(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateKafkaExporter(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_KafkaExportersServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListKafkaExporters': grpc.unary_unary_rpc_method_handler(
                    servicer.ListKafkaExporters,
                    request_deserializer=streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.ListKafkaExportersRequest.FromString,
                    response_serializer=streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.ListKafkaExportersResponse.SerializeToString,
            ),
            'GetKafkaExporter': grpc.unary_unary_rpc_method_handler(
                    servicer.GetKafkaExporter,
                    request_deserializer=streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.GetKafkaExporterRequest.FromString,
                    response_serializer=streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.GetKafkaExporterResponse.SerializeToString,
            ),
            'DeleteKafkaExporter': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteKafkaExporter,
                    request_deserializer=streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.DeleteKafkaExporterRequest.FromString,
                    response_serializer=streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.DeleteKafkaExporterResponse.SerializeToString,
            ),
            'CreateKafkaExporter': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateKafkaExporter,
                    request_deserializer=streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.CreateKafkaExporterRequest.FromString,
                    response_serializer=streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.CreateKafkaExporterResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'streammachine.api.kafka_exporters.v1.KafkaExportersService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class KafkaExportersService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListKafkaExporters(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/streammachine.api.kafka_exporters.v1.KafkaExportersService/ListKafkaExporters',
            streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.ListKafkaExportersRequest.SerializeToString,
            streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.ListKafkaExportersResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetKafkaExporter(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/streammachine.api.kafka_exporters.v1.KafkaExportersService/GetKafkaExporter',
            streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.GetKafkaExporterRequest.SerializeToString,
            streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.GetKafkaExporterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteKafkaExporter(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/streammachine.api.kafka_exporters.v1.KafkaExportersService/DeleteKafkaExporter',
            streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.DeleteKafkaExporterRequest.SerializeToString,
            streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.DeleteKafkaExporterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateKafkaExporter(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/streammachine.api.kafka_exporters.v1.KafkaExportersService/CreateKafkaExporter',
            streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.CreateKafkaExporterRequest.SerializeToString,
            streammachine_dot_api_dot_kafka__exporters_dot_v1_dot_kafka__exporters__v1__pb2.CreateKafkaExporterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
