"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.struct_pb2
import sys
import typing
import v0_messages_pb2
import v0_summaries_pb2

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _Op:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _OpEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_Op.ValueType], builtins.type):  # noqa: F821
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    unused: _Op.ValueType  # 0
    LT: _Op.ValueType  # 1
    LE: _Op.ValueType  # 2
    EQ: _Op.ValueType  # 3
    NE: _Op.ValueType  # 4
    GE: _Op.ValueType  # 5
    GT: _Op.ValueType  # 6
    MATCH: _Op.ValueType  # 7
    NOMATCH: _Op.ValueType  # 8
    BTWN: _Op.ValueType  # 9
    IN_SET: _Op.ValueType  # 10
    CONTAIN_SET: _Op.ValueType  # 11
    EQ_SET: _Op.ValueType  # 12
    APPLY_FUNC: _Op.ValueType  # 13
    IN: _Op.ValueType  # 14
    CONTAIN: _Op.ValueType  # 15
    NOT_IN: _Op.ValueType  # 16
    SUM: _Op.ValueType  # 17

class Op(_Op, metaclass=_OpEnumTypeWrapper):
    """constraints specify one of the following binary boolean relationships."""

unused: Op.ValueType  # 0
LT: Op.ValueType  # 1
LE: Op.ValueType  # 2
EQ: Op.ValueType  # 3
NE: Op.ValueType  # 4
GE: Op.ValueType  # 5
GT: Op.ValueType  # 6
MATCH: Op.ValueType  # 7
NOMATCH: Op.ValueType  # 8
BTWN: Op.ValueType  # 9
IN_SET: Op.ValueType  # 10
CONTAIN_SET: Op.ValueType  # 11
EQ_SET: Op.ValueType  # 12
APPLY_FUNC: Op.ValueType  # 13
IN: Op.ValueType  # 14
CONTAIN: Op.ValueType  # 15
NOT_IN: Op.ValueType  # 16
SUM: Op.ValueType  # 17
global___Op = Op

class SummaryConstraintMsg(google.protobuf.message.Message):
    """Summary constraints specify a relationship between a summary field and a literal value,
    or between two summary fields.
    e.g.     'min' < 6
    'std_dev' < 2.17
    'min' > 'avg'
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    FIRST_FIELD_FIELD_NUMBER: builtins.int
    SECOND_FIELD_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    BETWEEN_FIELD_NUMBER: builtins.int
    REFERENCE_SET_FIELD_NUMBER: builtins.int
    VALUE_STR_FIELD_NUMBER: builtins.int
    OP_FIELD_NUMBER: builtins.int
    VERBOSE_FIELD_NUMBER: builtins.int
    QUANTILE_VALUE_FIELD_NUMBER: builtins.int
    CONTINUOUS_DISTRIBUTION_FIELD_NUMBER: builtins.int
    DISCRETE_DISTRIBUTION_FIELD_NUMBER: builtins.int
    name: builtins.str
    first_field: builtins.str
    second_field: builtins.str
    value: builtins.float
    @property
    def between(self) -> global___SummaryBetweenConstraintMsg: ...
    @property
    def reference_set(self) -> google.protobuf.struct_pb2.ListValue: ...
    value_str: builtins.str
    op: global___Op.ValueType
    verbose: builtins.bool
    quantile_value: builtins.float
    @property
    def continuous_distribution(self) -> global___ReferenceDistributionContinuousMessage: ...
    @property
    def discrete_distribution(self) -> global___ReferenceDistributionDiscreteMessage: ...
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        first_field: builtins.str = ...,
        second_field: builtins.str = ...,
        value: builtins.float = ...,
        between: global___SummaryBetweenConstraintMsg | None = ...,
        reference_set: google.protobuf.struct_pb2.ListValue | None = ...,
        value_str: builtins.str = ...,
        op: global___Op.ValueType = ...,
        verbose: builtins.bool = ...,
        quantile_value: builtins.float = ...,
        continuous_distribution: global___ReferenceDistributionContinuousMessage | None = ...,
        discrete_distribution: global___ReferenceDistributionDiscreteMessage | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["between", b"between", "continuous_distribution", b"continuous_distribution", "discrete_distribution", b"discrete_distribution", "reference_distribution", b"reference_distribution", "reference_set", b"reference_set", "second", b"second", "second_field", b"second_field", "value", b"value", "value_str", b"value_str"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["between", b"between", "continuous_distribution", b"continuous_distribution", "discrete_distribution", b"discrete_distribution", "first_field", b"first_field", "name", b"name", "op", b"op", "quantile_value", b"quantile_value", "reference_distribution", b"reference_distribution", "reference_set", b"reference_set", "second", b"second", "second_field", b"second_field", "value", b"value", "value_str", b"value_str", "verbose", b"verbose"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["reference_distribution", b"reference_distribution"]) -> typing_extensions.Literal["continuous_distribution", "discrete_distribution"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["second", b"second"]) -> typing_extensions.Literal["second_field", "value", "between", "reference_set", "value_str"] | None: ...

global___SummaryConstraintMsg = SummaryConstraintMsg

class ReferenceDistributionContinuousMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SKETCH_FIELD_NUMBER: builtins.int
    @property
    def sketch(self) -> v0_messages_pb2.KllFloatsSketchMessage: ...
    def __init__(
        self,
        *,
        sketch: v0_messages_pb2.KllFloatsSketchMessage | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["sketch", b"sketch"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["sketch", b"sketch"]) -> None: ...

global___ReferenceDistributionContinuousMessage = ReferenceDistributionContinuousMessage

class ReferenceDistributionDiscreteMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FREQUENT_ITEMS_FIELD_NUMBER: builtins.int
    UNIQUE_COUNT_FIELD_NUMBER: builtins.int
    TOTAL_COUNT_FIELD_NUMBER: builtins.int
    @property
    def frequent_items(self) -> v0_summaries_pb2.FrequentItemsSummary: ...
    @property
    def unique_count(self) -> v0_summaries_pb2.UniqueCountSummary: ...
    total_count: builtins.float
    def __init__(
        self,
        *,
        frequent_items: v0_summaries_pb2.FrequentItemsSummary | None = ...,
        unique_count: v0_summaries_pb2.UniqueCountSummary | None = ...,
        total_count: builtins.float = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["frequent_items", b"frequent_items", "unique_count", b"unique_count"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["frequent_items", b"frequent_items", "total_count", b"total_count", "unique_count", b"unique_count"]) -> None: ...

global___ReferenceDistributionDiscreteMessage = ReferenceDistributionDiscreteMessage

class SummaryBetweenConstraintMsg(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SECOND_FIELD_FIELD_NUMBER: builtins.int
    LOWER_VALUE_FIELD_NUMBER: builtins.int
    THIRD_FIELD_FIELD_NUMBER: builtins.int
    UPPER_VALUE_FIELD_NUMBER: builtins.int
    second_field: builtins.str
    lower_value: builtins.float
    third_field: builtins.str
    upper_value: builtins.float
    def __init__(
        self,
        *,
        second_field: builtins.str = ...,
        lower_value: builtins.float = ...,
        third_field: builtins.str = ...,
        upper_value: builtins.float = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["lower", b"lower", "lower_value", b"lower_value", "second_field", b"second_field", "third_field", b"third_field", "upper", b"upper", "upper_value", b"upper_value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["lower", b"lower", "lower_value", b"lower_value", "second_field", b"second_field", "third_field", b"third_field", "upper", b"upper", "upper_value", b"upper_value"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["lower", b"lower"]) -> typing_extensions.Literal["second_field", "lower_value"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["upper", b"upper"]) -> typing_extensions.Literal["third_field", "upper_value"] | None: ...

global___SummaryBetweenConstraintMsg = SummaryBetweenConstraintMsg

class ApplyFunctionMsg(google.protobuf.message.Message):
    """ValueConstraints express a binary boolean relationship between an implied numeric value and a literal, or between a string value and a regex pattern.
    These are applied to every incoming value that is processed by whylogs.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FUNCTION_FIELD_NUMBER: builtins.int
    REFERENCE_VALUE_FIELD_NUMBER: builtins.int
    function: builtins.str
    reference_value: builtins.str
    def __init__(
        self,
        *,
        function: builtins.str = ...,
        reference_value: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["function", b"function", "reference_value", b"reference_value"]) -> None: ...

global___ApplyFunctionMsg = ApplyFunctionMsg

class ValueConstraintMsg(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    REGEX_PATTERN_FIELD_NUMBER: builtins.int
    VALUE_SET_FIELD_NUMBER: builtins.int
    FUNCTION_FIELD_NUMBER: builtins.int
    OP_FIELD_NUMBER: builtins.int
    VERBOSE_FIELD_NUMBER: builtins.int
    TOTAL_FIELD_NUMBER: builtins.int
    FAILURES_FIELD_NUMBER: builtins.int
    name: builtins.str
    value: builtins.float
    regex_pattern: builtins.str
    @property
    def value_set(self) -> google.protobuf.struct_pb2.ListValue: ...
    @property
    def function(self) -> global___ApplyFunctionMsg: ...
    op: global___Op.ValueType
    verbose: builtins.bool
    total: builtins.int
    failures: builtins.int
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        value: builtins.float = ...,
        regex_pattern: builtins.str = ...,
        value_set: google.protobuf.struct_pb2.ListValue | None = ...,
        function: global___ApplyFunctionMsg | None = ...,
        op: global___Op.ValueType = ...,
        verbose: builtins.bool = ...,
        total: builtins.int = ...,
        failures: builtins.int = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["function", b"function", "regex_pattern", b"regex_pattern", "second_field", b"second_field", "value", b"value", "value_set", b"value_set"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["failures", b"failures", "function", b"function", "name", b"name", "op", b"op", "regex_pattern", b"regex_pattern", "second_field", b"second_field", "total", b"total", "value", b"value", "value_set", b"value_set", "verbose", b"verbose"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["second_field", b"second_field"]) -> typing_extensions.Literal["value", "regex_pattern", "value_set", "function"] | None: ...

global___ValueConstraintMsg = ValueConstraintMsg

class MultiColumnValueConstraintMsg(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    DEPENDENT_COLUMNS_FIELD_NUMBER: builtins.int
    DEPENDENT_COLUMN_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    VALUE_SET_FIELD_NUMBER: builtins.int
    REFERENCE_COLUMNS_FIELD_NUMBER: builtins.int
    OP_FIELD_NUMBER: builtins.int
    VERBOSE_FIELD_NUMBER: builtins.int
    INTERNAL_DEPENDENT_COLUMNS_OP_FIELD_NUMBER: builtins.int
    TOTAL_FIELD_NUMBER: builtins.int
    FAILURES_FIELD_NUMBER: builtins.int
    name: builtins.str
    @property
    def dependent_columns(self) -> google.protobuf.struct_pb2.ListValue: ...
    dependent_column: builtins.str
    value: builtins.float
    @property
    def value_set(self) -> google.protobuf.struct_pb2.ListValue: ...
    @property
    def reference_columns(self) -> google.protobuf.struct_pb2.ListValue: ...
    op: global___Op.ValueType
    verbose: builtins.bool
    internal_dependent_columns_op: global___Op.ValueType
    total: builtins.int
    failures: builtins.int
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        dependent_columns: google.protobuf.struct_pb2.ListValue | None = ...,
        dependent_column: builtins.str = ...,
        value: builtins.float = ...,
        value_set: google.protobuf.struct_pb2.ListValue | None = ...,
        reference_columns: google.protobuf.struct_pb2.ListValue | None = ...,
        op: global___Op.ValueType = ...,
        verbose: builtins.bool = ...,
        internal_dependent_columns_op: global___Op.ValueType = ...,
        total: builtins.int = ...,
        failures: builtins.int = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["dependent", b"dependent", "dependent_column", b"dependent_column", "dependent_columns", b"dependent_columns", "reference", b"reference", "reference_columns", b"reference_columns", "value", b"value", "value_set", b"value_set"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["dependent", b"dependent", "dependent_column", b"dependent_column", "dependent_columns", b"dependent_columns", "failures", b"failures", "internal_dependent_columns_op", b"internal_dependent_columns_op", "name", b"name", "op", b"op", "reference", b"reference", "reference_columns", b"reference_columns", "total", b"total", "value", b"value", "value_set", b"value_set", "verbose", b"verbose"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["dependent", b"dependent"]) -> typing_extensions.Literal["dependent_columns", "dependent_column"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["reference", b"reference"]) -> typing_extensions.Literal["value", "value_set", "reference_columns"] | None: ...

global___MultiColumnValueConstraintMsg = MultiColumnValueConstraintMsg

class ValueConstraintMsgs(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONSTRAINTS_FIELD_NUMBER: builtins.int
    MULTI_COLUMN_CONSTRAINTS_FIELD_NUMBER: builtins.int
    @property
    def constraints(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ValueConstraintMsg]: ...
    @property
    def multi_column_constraints(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___MultiColumnValueConstraintMsg]: ...
    def __init__(
        self,
        *,
        constraints: collections.abc.Iterable[global___ValueConstraintMsg] | None = ...,
        multi_column_constraints: collections.abc.Iterable[global___MultiColumnValueConstraintMsg] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["constraints", b"constraints", "multi_column_constraints", b"multi_column_constraints"]) -> None: ...

global___ValueConstraintMsgs = ValueConstraintMsgs

class SummaryConstraintMsgs(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONSTRAINTS_FIELD_NUMBER: builtins.int
    @property
    def constraints(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___SummaryConstraintMsg]: ...
    def __init__(
        self,
        *,
        constraints: collections.abc.Iterable[global___SummaryConstraintMsg] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["constraints", b"constraints"]) -> None: ...

global___SummaryConstraintMsgs = SummaryConstraintMsgs

class DatasetConstraintMsg(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class ValueConstraintsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___ValueConstraintMsgs: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___ValueConstraintMsgs | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    class SummaryConstraintsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___SummaryConstraintMsgs: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___SummaryConstraintMsgs | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    PROPERTIES_FIELD_NUMBER: builtins.int
    VALUE_CONSTRAINTS_FIELD_NUMBER: builtins.int
    SUMMARY_CONSTRAINTS_FIELD_NUMBER: builtins.int
    TABLE_SHAPE_CONSTRAINTS_FIELD_NUMBER: builtins.int
    MULTI_COLUMN_VALUE_CONSTRAINTS_FIELD_NUMBER: builtins.int
    @property
    def properties(self) -> v0_messages_pb2.DatasetPropertiesV0: ...
    @property
    def value_constraints(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___ValueConstraintMsgs]: ...
    @property
    def summary_constraints(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___SummaryConstraintMsgs]: ...
    @property
    def table_shape_constraints(self) -> global___SummaryConstraintMsgs: ...
    @property
    def multi_column_value_constraints(self) -> global___ValueConstraintMsgs: ...
    def __init__(
        self,
        *,
        properties: v0_messages_pb2.DatasetPropertiesV0 | None = ...,
        value_constraints: collections.abc.Mapping[builtins.str, global___ValueConstraintMsgs] | None = ...,
        summary_constraints: collections.abc.Mapping[builtins.str, global___SummaryConstraintMsgs] | None = ...,
        table_shape_constraints: global___SummaryConstraintMsgs | None = ...,
        multi_column_value_constraints: global___ValueConstraintMsgs | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["multi_column_value_constraints", b"multi_column_value_constraints", "properties", b"properties", "table_shape_constraints", b"table_shape_constraints"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["multi_column_value_constraints", b"multi_column_value_constraints", "properties", b"properties", "summary_constraints", b"summary_constraints", "table_shape_constraints", b"table_shape_constraints", "value_constraints", b"value_constraints"]) -> None: ...

global___DatasetConstraintMsg = DatasetConstraintMsg
