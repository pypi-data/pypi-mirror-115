# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tendermint/libs/bits/types.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tendermint/libs/bits/types.proto',
  package='tendermint.libs.bits',
  syntax='proto3',
  serialized_options=b'Z;github.com/tendermint/tendermint/proto/tendermint/libs/bits',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n tendermint/libs/bits/types.proto\x12\x14tendermint.libs.bits\"\'\n\x08\x42itArray\x12\x0c\n\x04\x62its\x18\x01 \x01(\x03\x12\r\n\x05\x65lems\x18\x02 \x03(\x04\x42=Z;github.com/tendermint/tendermint/proto/tendermint/libs/bitsb\x06proto3'
)




_BITARRAY = _descriptor.Descriptor(
  name='BitArray',
  full_name='tendermint.libs.bits.BitArray',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='bits', full_name='tendermint.libs.bits.BitArray.bits', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='elems', full_name='tendermint.libs.bits.BitArray.elems', index=1,
      number=2, type=4, cpp_type=4, label=3,
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
  serialized_start=58,
  serialized_end=97,
)

DESCRIPTOR.message_types_by_name['BitArray'] = _BITARRAY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BitArray = _reflection.GeneratedProtocolMessageType('BitArray', (_message.Message,), {
  'DESCRIPTOR' : _BITARRAY,
  '__module__' : 'tendermint.libs.bits.types_pb2'
  # @@protoc_insertion_point(class_scope:tendermint.libs.bits.BitArray)
  })
_sym_db.RegisterMessage(BitArray)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
