# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: streammachine/api/event_contracts/v1/event_contracts_v1.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from streammachine.api.entities.v1 import entities_v1_pb2 as streammachine_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='streammachine/api/event_contracts/v1/event_contracts_v1.proto',
  package='streammachine.api.event_contracts.v1',
  syntax='proto3',
  serialized_options=b'\n\'io.streammachine.api.event_contracts.v1P\001ZTgithub.com/streammachineio/api-definitions-go/api/event_contracts/v1;event_contracts',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n=streammachine/api/event_contracts/v1/event_contracts_v1.proto\x12$streammachine.api.event_contracts.v1\x1a/streammachine/api/entities/v1/entities_v1.proto\"?\n\x19ListEventContractsRequest\x12\x12\n\nbilling_id\x18\x01 \x01(\t\x12\x0e\n\x06\x66ilter\x18\x02 \x01(\t\"c\n\x1aListEventContractsResponse\x12\x45\n\x0f\x65vent_contracts\x18\x01 \x03(\x0b\x32,.streammachine.api.entities.v1.EventContract\"v\n\x1a\x43reateEventContractRequest\x12\x12\n\nbilling_id\x18\x01 \x01(\t\x12\x44\n\x0e\x65vent_contract\x18\x02 \x01(\x0b\x32,.streammachine.api.entities.v1.EventContract\"c\n\x1b\x43reateEventContractResponse\x12\x44\n\x0e\x65vent_contract\x18\x01 \x01(\x0b\x32,.streammachine.api.entities.v1.EventContract\"k\n\x17GetEventContractRequest\x12\x12\n\nbilling_id\x18\x01 \x01(\t\x12<\n\x03ref\x18\x02 \x01(\x0b\x32/.streammachine.api.entities.v1.EventContractRef\"`\n\x18GetEventContractResponse\x12\x44\n\x0e\x65vent_contract\x18\x01 \x01(\x0b\x32,.streammachine.api.entities.v1.EventContract2\xe2\x03\n\x15\x45ventContractsService\x12\x97\x01\n\x12ListEventContracts\x12?.streammachine.api.event_contracts.v1.ListEventContractsRequest\x1a@.streammachine.api.event_contracts.v1.ListEventContractsResponse\x12\x91\x01\n\x10GetEventContract\x12=.streammachine.api.event_contracts.v1.GetEventContractRequest\x1a>.streammachine.api.event_contracts.v1.GetEventContractResponse\x12\x9a\x01\n\x13\x43reateEventContract\x12@.streammachine.api.event_contracts.v1.CreateEventContractRequest\x1a\x41.streammachine.api.event_contracts.v1.CreateEventContractResponseB\x81\x01\n\'io.streammachine.api.event_contracts.v1P\x01ZTgithub.com/streammachineio/api-definitions-go/api/event_contracts/v1;event_contractsb\x06proto3'
  ,
  dependencies=[streammachine_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2.DESCRIPTOR,])




_LISTEVENTCONTRACTSREQUEST = _descriptor.Descriptor(
  name='ListEventContractsRequest',
  full_name='streammachine.api.event_contracts.v1.ListEventContractsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='billing_id', full_name='streammachine.api.event_contracts.v1.ListEventContractsRequest.billing_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filter', full_name='streammachine.api.event_contracts.v1.ListEventContractsRequest.filter', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=152,
  serialized_end=215,
)


_LISTEVENTCONTRACTSRESPONSE = _descriptor.Descriptor(
  name='ListEventContractsResponse',
  full_name='streammachine.api.event_contracts.v1.ListEventContractsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='event_contracts', full_name='streammachine.api.event_contracts.v1.ListEventContractsResponse.event_contracts', index=0,
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
  serialized_start=217,
  serialized_end=316,
)


_CREATEEVENTCONTRACTREQUEST = _descriptor.Descriptor(
  name='CreateEventContractRequest',
  full_name='streammachine.api.event_contracts.v1.CreateEventContractRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='billing_id', full_name='streammachine.api.event_contracts.v1.CreateEventContractRequest.billing_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='event_contract', full_name='streammachine.api.event_contracts.v1.CreateEventContractRequest.event_contract', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_start=318,
  serialized_end=436,
)


_CREATEEVENTCONTRACTRESPONSE = _descriptor.Descriptor(
  name='CreateEventContractResponse',
  full_name='streammachine.api.event_contracts.v1.CreateEventContractResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='event_contract', full_name='streammachine.api.event_contracts.v1.CreateEventContractResponse.event_contract', index=0,
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
  serialized_start=438,
  serialized_end=537,
)


_GETEVENTCONTRACTREQUEST = _descriptor.Descriptor(
  name='GetEventContractRequest',
  full_name='streammachine.api.event_contracts.v1.GetEventContractRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='billing_id', full_name='streammachine.api.event_contracts.v1.GetEventContractRequest.billing_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ref', full_name='streammachine.api.event_contracts.v1.GetEventContractRequest.ref', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_start=539,
  serialized_end=646,
)


_GETEVENTCONTRACTRESPONSE = _descriptor.Descriptor(
  name='GetEventContractResponse',
  full_name='streammachine.api.event_contracts.v1.GetEventContractResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='event_contract', full_name='streammachine.api.event_contracts.v1.GetEventContractResponse.event_contract', index=0,
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
  serialized_start=648,
  serialized_end=744,
)

_LISTEVENTCONTRACTSRESPONSE.fields_by_name['event_contracts'].message_type = streammachine_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._EVENTCONTRACT
_CREATEEVENTCONTRACTREQUEST.fields_by_name['event_contract'].message_type = streammachine_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._EVENTCONTRACT
_CREATEEVENTCONTRACTRESPONSE.fields_by_name['event_contract'].message_type = streammachine_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._EVENTCONTRACT
_GETEVENTCONTRACTREQUEST.fields_by_name['ref'].message_type = streammachine_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._EVENTCONTRACTREF
_GETEVENTCONTRACTRESPONSE.fields_by_name['event_contract'].message_type = streammachine_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._EVENTCONTRACT
DESCRIPTOR.message_types_by_name['ListEventContractsRequest'] = _LISTEVENTCONTRACTSREQUEST
DESCRIPTOR.message_types_by_name['ListEventContractsResponse'] = _LISTEVENTCONTRACTSRESPONSE
DESCRIPTOR.message_types_by_name['CreateEventContractRequest'] = _CREATEEVENTCONTRACTREQUEST
DESCRIPTOR.message_types_by_name['CreateEventContractResponse'] = _CREATEEVENTCONTRACTRESPONSE
DESCRIPTOR.message_types_by_name['GetEventContractRequest'] = _GETEVENTCONTRACTREQUEST
DESCRIPTOR.message_types_by_name['GetEventContractResponse'] = _GETEVENTCONTRACTRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ListEventContractsRequest = _reflection.GeneratedProtocolMessageType('ListEventContractsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTEVENTCONTRACTSREQUEST,
  '__module__' : 'streammachine.api.event_contracts.v1.event_contracts_v1_pb2'
  # @@protoc_insertion_point(class_scope:streammachine.api.event_contracts.v1.ListEventContractsRequest)
  })
_sym_db.RegisterMessage(ListEventContractsRequest)

ListEventContractsResponse = _reflection.GeneratedProtocolMessageType('ListEventContractsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTEVENTCONTRACTSRESPONSE,
  '__module__' : 'streammachine.api.event_contracts.v1.event_contracts_v1_pb2'
  # @@protoc_insertion_point(class_scope:streammachine.api.event_contracts.v1.ListEventContractsResponse)
  })
_sym_db.RegisterMessage(ListEventContractsResponse)

CreateEventContractRequest = _reflection.GeneratedProtocolMessageType('CreateEventContractRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEEVENTCONTRACTREQUEST,
  '__module__' : 'streammachine.api.event_contracts.v1.event_contracts_v1_pb2'
  # @@protoc_insertion_point(class_scope:streammachine.api.event_contracts.v1.CreateEventContractRequest)
  })
_sym_db.RegisterMessage(CreateEventContractRequest)

CreateEventContractResponse = _reflection.GeneratedProtocolMessageType('CreateEventContractResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEEVENTCONTRACTRESPONSE,
  '__module__' : 'streammachine.api.event_contracts.v1.event_contracts_v1_pb2'
  # @@protoc_insertion_point(class_scope:streammachine.api.event_contracts.v1.CreateEventContractResponse)
  })
_sym_db.RegisterMessage(CreateEventContractResponse)

GetEventContractRequest = _reflection.GeneratedProtocolMessageType('GetEventContractRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETEVENTCONTRACTREQUEST,
  '__module__' : 'streammachine.api.event_contracts.v1.event_contracts_v1_pb2'
  # @@protoc_insertion_point(class_scope:streammachine.api.event_contracts.v1.GetEventContractRequest)
  })
_sym_db.RegisterMessage(GetEventContractRequest)

GetEventContractResponse = _reflection.GeneratedProtocolMessageType('GetEventContractResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETEVENTCONTRACTRESPONSE,
  '__module__' : 'streammachine.api.event_contracts.v1.event_contracts_v1_pb2'
  # @@protoc_insertion_point(class_scope:streammachine.api.event_contracts.v1.GetEventContractResponse)
  })
_sym_db.RegisterMessage(GetEventContractResponse)


DESCRIPTOR._options = None

_EVENTCONTRACTSSERVICE = _descriptor.ServiceDescriptor(
  name='EventContractsService',
  full_name='streammachine.api.event_contracts.v1.EventContractsService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=747,
  serialized_end=1229,
  methods=[
  _descriptor.MethodDescriptor(
    name='ListEventContracts',
    full_name='streammachine.api.event_contracts.v1.EventContractsService.ListEventContracts',
    index=0,
    containing_service=None,
    input_type=_LISTEVENTCONTRACTSREQUEST,
    output_type=_LISTEVENTCONTRACTSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetEventContract',
    full_name='streammachine.api.event_contracts.v1.EventContractsService.GetEventContract',
    index=1,
    containing_service=None,
    input_type=_GETEVENTCONTRACTREQUEST,
    output_type=_GETEVENTCONTRACTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CreateEventContract',
    full_name='streammachine.api.event_contracts.v1.EventContractsService.CreateEventContract',
    index=2,
    containing_service=None,
    input_type=_CREATEEVENTCONTRACTREQUEST,
    output_type=_CREATEEVENTCONTRACTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_EVENTCONTRACTSSERVICE)

DESCRIPTOR.services_by_name['EventContractsService'] = _EVENTCONTRACTSSERVICE

# @@protoc_insertion_point(module_scope)
