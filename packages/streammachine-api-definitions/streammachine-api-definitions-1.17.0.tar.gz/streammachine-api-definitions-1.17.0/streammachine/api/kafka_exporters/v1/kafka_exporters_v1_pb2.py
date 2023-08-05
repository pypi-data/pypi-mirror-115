# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: streammachine/api/kafka_exporters/v1/kafka_exporters_v1.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from streammachine.api.entities.v1 import entities_v1_pb2 as streammachine_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='streammachine/api/kafka_exporters/v1/kafka_exporters_v1.proto',
  package='streammachine.api.kafka_exporters.v1',
  syntax='proto3',
  serialized_options=b'\n\'io.streammachine.api.kafka_exporters.v1P\001ZTgithub.com/streammachineio/api-definitions-go/api/kafka_exporters/v1;kafka_exporters',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n=streammachine/api/kafka_exporters/v1/kafka_exporters_v1.proto\x12$streammachine.api.kafka_exporters.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a/streammachine/api/entities/v1/entities_v1.proto\"4\n\x19ListKafkaExportersRequest\x12\x17\n\nbilling_id\x18\x01 \x01(\tB\x03\xe0\x41\x03\"c\n\x1aListKafkaExportersResponse\x12\x45\n\x0fkafka_exporters\x18\x01 \x03(\x0b\x32,.streammachine.api.entities.v1.KafkaExporter\"w\n\x1a\x44\x65leteKafkaExporterRequest\x12\x41\n\x03ref\x18\x01 \x01(\x0b\x32/.streammachine.api.entities.v1.KafkaExporterRefB\x03\xe0\x41\x02\x12\x16\n\trecursive\x18\x02 \x01(\x08\x42\x03\xe0\x41\x02\"\x1d\n\x1b\x44\x65leteKafkaExporterResponse\"g\n\x1a\x43reateKafkaExporterRequest\x12I\n\x0ekafka_exporter\x18\x01 \x01(\x0b\x32,.streammachine.api.entities.v1.KafkaExporterB\x03\xe0\x41\x02\"c\n\x1b\x43reateKafkaExporterResponse\x12\x44\n\x0ekafka_exporter\x18\x01 \x01(\x0b\x32,.streammachine.api.entities.v1.KafkaExporter\"\\\n\x17GetKafkaExporterRequest\x12\x41\n\x03ref\x18\x01 \x01(\x0b\x32/.streammachine.api.entities.v1.KafkaExporterRefB\x03\xe0\x41\x02\"`\n\x18GetKafkaExporterResponse\x12\x44\n\x0ekafka_exporter\x18\x01 \x01(\x0b\x32,.streammachine.api.entities.v1.KafkaExporter2\xff\x04\n\x15KafkaExportersService\x12\x97\x01\n\x12ListKafkaExporters\x12?.streammachine.api.kafka_exporters.v1.ListKafkaExportersRequest\x1a@.streammachine.api.kafka_exporters.v1.ListKafkaExportersResponse\x12\x91\x01\n\x10GetKafkaExporter\x12=.streammachine.api.kafka_exporters.v1.GetKafkaExporterRequest\x1a>.streammachine.api.kafka_exporters.v1.GetKafkaExporterResponse\x12\x9a\x01\n\x13\x44\x65leteKafkaExporter\x12@.streammachine.api.kafka_exporters.v1.DeleteKafkaExporterRequest\x1a\x41.streammachine.api.kafka_exporters.v1.DeleteKafkaExporterResponse\x12\x9a\x01\n\x13\x43reateKafkaExporter\x12@.streammachine.api.kafka_exporters.v1.CreateKafkaExporterRequest\x1a\x41.streammachine.api.kafka_exporters.v1.CreateKafkaExporterResponseB\x81\x01\n\'io.streammachine.api.kafka_exporters.v1P\x01ZTgithub.com/streammachineio/api-definitions-go/api/kafka_exporters/v1;kafka_exportersb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,streammachine_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2.DESCRIPTOR,])




_LISTKAFKAEXPORTERSREQUEST = _descriptor.Descriptor(
  name='ListKafkaExportersRequest',
  full_name='streammachine.api.kafka_exporters.v1.ListKafkaExportersRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='billing_id', full_name='streammachine.api.kafka_exporters.v1.ListKafkaExportersRequest.billing_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=185,
  serialized_end=237,
)


_LISTKAFKAEXPORTERSRESPONSE = _descriptor.Descriptor(
  name='ListKafkaExportersResponse',
  full_name='streammachine.api.kafka_exporters.v1.ListKafkaExportersResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='kafka_exporters', full_name='streammachine.api.kafka_exporters.v1.ListKafkaExportersResponse.kafka_exporters', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=239,
  serialized_end=338,
)


_DELETEKAFKAEXPORTERREQUEST = _descriptor.Descriptor(
  name='DeleteKafkaExporterRequest',
  full_name='streammachine.api.kafka_exporters.v1.DeleteKafkaExporterRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ref', full_name='streammachine.api.kafka_exporters.v1.DeleteKafkaExporterRequest.ref', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\002', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='recursive', full_name='streammachine.api.kafka_exporters.v1.DeleteKafkaExporterRequest.recursive', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\002', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=340,
  serialized_end=459,
)


_DELETEKAFKAEXPORTERRESPONSE = _descriptor.Descriptor(
  name='DeleteKafkaExporterResponse',
  full_name='streammachine.api.kafka_exporters.v1.DeleteKafkaExporterResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=461,
  serialized_end=490,
)


_CREATEKAFKAEXPORTERREQUEST = _descriptor.Descriptor(
  name='CreateKafkaExporterRequest',
  full_name='streammachine.api.kafka_exporters.v1.CreateKafkaExporterRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='kafka_exporter', full_name='streammachine.api.kafka_exporters.v1.CreateKafkaExporterRequest.kafka_exporter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\002', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=492,
  serialized_end=595,
)


_CREATEKAFKAEXPORTERRESPONSE = _descriptor.Descriptor(
  name='CreateKafkaExporterResponse',
  full_name='streammachine.api.kafka_exporters.v1.CreateKafkaExporterResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='kafka_exporter', full_name='streammachine.api.kafka_exporters.v1.CreateKafkaExporterResponse.kafka_exporter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=597,
  serialized_end=696,
)


_GETKAFKAEXPORTERREQUEST = _descriptor.Descriptor(
  name='GetKafkaExporterRequest',
  full_name='streammachine.api.kafka_exporters.v1.GetKafkaExporterRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ref', full_name='streammachine.api.kafka_exporters.v1.GetKafkaExporterRequest.ref', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\002', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=698,
  serialized_end=790,
)


_GETKAFKAEXPORTERRESPONSE = _descriptor.Descriptor(
  name='GetKafkaExporterResponse',
  full_name='streammachine.api.kafka_exporters.v1.GetKafkaExporterResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='kafka_exporter', full_name='streammachine.api.kafka_exporters.v1.GetKafkaExporterResponse.kafka_exporter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=792,
  serialized_end=888,
)

_LISTKAFKAEXPORTERSRESPONSE.fields_by_name['kafka_exporters'].message_type = streammachine_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._KAFKAEXPORTER
_DELETEKAFKAEXPORTERREQUEST.fields_by_name['ref'].message_type = streammachine_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._KAFKAEXPORTERREF
_CREATEKAFKAEXPORTERREQUEST.fields_by_name['kafka_exporter'].message_type = streammachine_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._KAFKAEXPORTER
_CREATEKAFKAEXPORTERRESPONSE.fields_by_name['kafka_exporter'].message_type = streammachine_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._KAFKAEXPORTER
_GETKAFKAEXPORTERREQUEST.fields_by_name['ref'].message_type = streammachine_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._KAFKAEXPORTERREF
_GETKAFKAEXPORTERRESPONSE.fields_by_name['kafka_exporter'].message_type = streammachine_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._KAFKAEXPORTER
DESCRIPTOR.message_types_by_name['ListKafkaExportersRequest'] = _LISTKAFKAEXPORTERSREQUEST
DESCRIPTOR.message_types_by_name['ListKafkaExportersResponse'] = _LISTKAFKAEXPORTERSRESPONSE
DESCRIPTOR.message_types_by_name['DeleteKafkaExporterRequest'] = _DELETEKAFKAEXPORTERREQUEST
DESCRIPTOR.message_types_by_name['DeleteKafkaExporterResponse'] = _DELETEKAFKAEXPORTERRESPONSE
DESCRIPTOR.message_types_by_name['CreateKafkaExporterRequest'] = _CREATEKAFKAEXPORTERREQUEST
DESCRIPTOR.message_types_by_name['CreateKafkaExporterResponse'] = _CREATEKAFKAEXPORTERRESPONSE
DESCRIPTOR.message_types_by_name['GetKafkaExporterRequest'] = _GETKAFKAEXPORTERREQUEST
DESCRIPTOR.message_types_by_name['GetKafkaExporterResponse'] = _GETKAFKAEXPORTERRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ListKafkaExportersRequest = _reflection.GeneratedProtocolMessageType('ListKafkaExportersRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTKAFKAEXPORTERSREQUEST,
  '__module__' : 'streammachine.api.kafka_exporters.v1.kafka_exporters_v1_pb2'
  # @@protoc_insertion_point(class_scope:streammachine.api.kafka_exporters.v1.ListKafkaExportersRequest)
  })
_sym_db.RegisterMessage(ListKafkaExportersRequest)

ListKafkaExportersResponse = _reflection.GeneratedProtocolMessageType('ListKafkaExportersResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTKAFKAEXPORTERSRESPONSE,
  '__module__' : 'streammachine.api.kafka_exporters.v1.kafka_exporters_v1_pb2'
  # @@protoc_insertion_point(class_scope:streammachine.api.kafka_exporters.v1.ListKafkaExportersResponse)
  })
_sym_db.RegisterMessage(ListKafkaExportersResponse)

DeleteKafkaExporterRequest = _reflection.GeneratedProtocolMessageType('DeleteKafkaExporterRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEKAFKAEXPORTERREQUEST,
  '__module__' : 'streammachine.api.kafka_exporters.v1.kafka_exporters_v1_pb2'
  # @@protoc_insertion_point(class_scope:streammachine.api.kafka_exporters.v1.DeleteKafkaExporterRequest)
  })
_sym_db.RegisterMessage(DeleteKafkaExporterRequest)

DeleteKafkaExporterResponse = _reflection.GeneratedProtocolMessageType('DeleteKafkaExporterResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETEKAFKAEXPORTERRESPONSE,
  '__module__' : 'streammachine.api.kafka_exporters.v1.kafka_exporters_v1_pb2'
  # @@protoc_insertion_point(class_scope:streammachine.api.kafka_exporters.v1.DeleteKafkaExporterResponse)
  })
_sym_db.RegisterMessage(DeleteKafkaExporterResponse)

CreateKafkaExporterRequest = _reflection.GeneratedProtocolMessageType('CreateKafkaExporterRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEKAFKAEXPORTERREQUEST,
  '__module__' : 'streammachine.api.kafka_exporters.v1.kafka_exporters_v1_pb2'
  # @@protoc_insertion_point(class_scope:streammachine.api.kafka_exporters.v1.CreateKafkaExporterRequest)
  })
_sym_db.RegisterMessage(CreateKafkaExporterRequest)

CreateKafkaExporterResponse = _reflection.GeneratedProtocolMessageType('CreateKafkaExporterResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEKAFKAEXPORTERRESPONSE,
  '__module__' : 'streammachine.api.kafka_exporters.v1.kafka_exporters_v1_pb2'
  # @@protoc_insertion_point(class_scope:streammachine.api.kafka_exporters.v1.CreateKafkaExporterResponse)
  })
_sym_db.RegisterMessage(CreateKafkaExporterResponse)

GetKafkaExporterRequest = _reflection.GeneratedProtocolMessageType('GetKafkaExporterRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETKAFKAEXPORTERREQUEST,
  '__module__' : 'streammachine.api.kafka_exporters.v1.kafka_exporters_v1_pb2'
  # @@protoc_insertion_point(class_scope:streammachine.api.kafka_exporters.v1.GetKafkaExporterRequest)
  })
_sym_db.RegisterMessage(GetKafkaExporterRequest)

GetKafkaExporterResponse = _reflection.GeneratedProtocolMessageType('GetKafkaExporterResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETKAFKAEXPORTERRESPONSE,
  '__module__' : 'streammachine.api.kafka_exporters.v1.kafka_exporters_v1_pb2'
  # @@protoc_insertion_point(class_scope:streammachine.api.kafka_exporters.v1.GetKafkaExporterResponse)
  })
_sym_db.RegisterMessage(GetKafkaExporterResponse)


DESCRIPTOR._options = None
_LISTKAFKAEXPORTERSREQUEST.fields_by_name['billing_id']._options = None
_DELETEKAFKAEXPORTERREQUEST.fields_by_name['ref']._options = None
_DELETEKAFKAEXPORTERREQUEST.fields_by_name['recursive']._options = None
_CREATEKAFKAEXPORTERREQUEST.fields_by_name['kafka_exporter']._options = None
_GETKAFKAEXPORTERREQUEST.fields_by_name['ref']._options = None

_KAFKAEXPORTERSSERVICE = _descriptor.ServiceDescriptor(
  name='KafkaExportersService',
  full_name='streammachine.api.kafka_exporters.v1.KafkaExportersService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=891,
  serialized_end=1530,
  methods=[
  _descriptor.MethodDescriptor(
    name='ListKafkaExporters',
    full_name='streammachine.api.kafka_exporters.v1.KafkaExportersService.ListKafkaExporters',
    index=0,
    containing_service=None,
    input_type=_LISTKAFKAEXPORTERSREQUEST,
    output_type=_LISTKAFKAEXPORTERSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetKafkaExporter',
    full_name='streammachine.api.kafka_exporters.v1.KafkaExportersService.GetKafkaExporter',
    index=1,
    containing_service=None,
    input_type=_GETKAFKAEXPORTERREQUEST,
    output_type=_GETKAFKAEXPORTERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DeleteKafkaExporter',
    full_name='streammachine.api.kafka_exporters.v1.KafkaExportersService.DeleteKafkaExporter',
    index=2,
    containing_service=None,
    input_type=_DELETEKAFKAEXPORTERREQUEST,
    output_type=_DELETEKAFKAEXPORTERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CreateKafkaExporter',
    full_name='streammachine.api.kafka_exporters.v1.KafkaExportersService.CreateKafkaExporter',
    index=3,
    containing_service=None,
    input_type=_CREATEKAFKAEXPORTERREQUEST,
    output_type=_CREATEKAFKAEXPORTERRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_KAFKAEXPORTERSSERVICE)

DESCRIPTOR.services_by_name['KafkaExportersService'] = _KAFKAEXPORTERSSERVICE

# @@protoc_insertion_point(module_scope)
