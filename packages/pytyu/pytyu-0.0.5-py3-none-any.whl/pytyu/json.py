"""Utilities to type checking JSON."""

from collections.abc import Mapping, Sequence
from inspect import get_annotations
import logging
from typing import Optional, TypeGuard, TypeVar

JSONKey = str
"""JSON key data type."""

JSONValue = (
    str
    | int
    | float
    | bool
    | None
    # Once mypy is able to handle recursive type aliases, we can replace `object` with
    # `JSONValue` in the next two types
    | Mapping[JSONKey, object]
    | Sequence[object]
)
"""JSON value data type."""

JSONObject = Mapping[JSONKey, JSONValue]
"""JSON dictionary value data type."""

JSONList = Sequence[JSONValue]
"""JSON list value data type."""

JSON = Mapping[JSONKey, JSONValue]
"""JSON data type."""

_JSONSimpleValue = Optional[str | int | float | bool]
_JSONComplexValue = JSONObject | JSONList


def _is_json_key(key: object) -> TypeGuard[JSONKey]:
    """Narrow `object` to `str` type."""
    return isinstance(key, JSONKey)


def _is_json_simple_value(value: object) -> TypeGuard[_JSONSimpleValue]:
    """Narrow `object` to `_JSONSimpleValue` types."""
    # https://github.com/python/mypy/issues/12155
    return isinstance(value, _JSONSimpleValue)  # type: ignore


def _is_json_object_value(value: object) -> TypeGuard[JSONObject]:
    """Narrow `object` to `JSONObject` types."""
    if isinstance(value, Mapping):
        return is_json(value)
    return False


def _is_json_list_value(value: object) -> TypeGuard[JSONList]:
    """Narrow `object` to `JSONList` types."""
    if isinstance(value, Sequence):
        return all(_is_json_value(maybe_json_value) for maybe_json_value in value)
    return False


def _is_json_complex_value(value: object) -> TypeGuard[_JSONComplexValue]:
    """Narrow `object` to `JSONObject | JSONList` types."""
    return _is_json_object_value(value) or _is_json_list_value(value)


def _is_json_value(value: object) -> TypeGuard[JSONValue]:
    """Narrow `object` to `JSONValue` type."""
    return _is_json_simple_value(value) or _is_json_complex_value(value)


def is_json(value: object) -> TypeGuard[JSON]:
    """Narrow `object` to `JSON` type."""
    if not isinstance(value, Mapping):
        return False
    return all(
        _is_json_key(maybe_json_key) and _is_json_value(maybe_json_value)
        for maybe_json_key, maybe_json_value in value.items()
    )


TypeT = TypeVar("TypeT", bound=type)


def _is_json_schema_simple(key: str, value: object, schema: TypeT) -> bool:
    """
    If `value` corresponding to `key` is a simple JSON value, check that it matches
    the `schema[key]` type.
    """
    if not _is_json_simple_value(value):
        return False

    try:
        key_type = get_annotations(schema)[key]
    except KeyError:
        logger.debug("Missing key: %s['%s']", schema, key)
        return False

    if not isinstance(value, key_type):
        logger.debug(
            "Wrong type: %s['%s']: %s = %s: %s",
            schema,
            key,
            key_type,
            value,
            type(value),
        )
        return False
    return True


def _is_json_schema_list(  # pylint: disable=too-many-return-statements
    key: str, value: object, schema: TypeT
) -> bool:
    """
    If `value` corresponding to `key` is a JSON list value, check that `schema[key]`
    is a generic list, and each item in `value` matches the `schema[key]` list type.
    """
    if not isinstance(value, Sequence) or isinstance(value, str):
        return False

    try:
        key_type = get_annotations(schema)[key]
    except KeyError:
        logger.debug("Missing key: %s['%s']", schema, key)
        return False

    key_origin_type = getattr(key_type, "__origin__", type(None))
    if not issubclass(key_origin_type, Sequence):
        logger.debug("Sequence not expected: %s['%s']: %s", schema, key, key_type)
        return False

    key_generic_params = getattr(key_type, "__args__", type(None))
    if not isinstance(key_generic_params, Sequence):
        logger.debug("Missing generic parameters: %s['%s']: %s", schema, key, key_type)
        return False

    key_generic_params_len = len(key_generic_params)
    if key_generic_params_len != 1:
        logger.debug(
            "Expected 1 generic Sequence parameter: %s['%s']: %s", schema, key, key_type
        )
        return False

    key_generic_param = key_generic_params[0]
    try:
        is_key_generic_param_mapping = issubclass(key_generic_param, Mapping)
    except TypeError:
        is_key_generic_param_mapping = False

    for each_value in value:
        if is_key_generic_param_mapping:
            if not is_json_schema(each_value, key_generic_param):
                return False
        elif not isinstance(each_value, key_generic_param):
            logger.debug(
                "Wrong type: %s['%s']: %s[%s] = [%s: %s]",
                schema,
                key,
                key_origin_type,
                key_generic_param,
                each_value,
                type(each_value),
            )
            return False
    return True


def is_json_schema(  # pylint: disable=too-many-return-statements
    value: object, schema: TypeT
) -> TypeGuard[TypeT]:
    """Narrow `value` to `schema` type."""
    if not isinstance(value, Mapping):
        return False

    for maybe_json_key, maybe_json_value in value.items():
        if not _is_json_key(maybe_json_key):
            return False

        if not (
            _is_json_schema_simple(maybe_json_key, maybe_json_value, schema)
            or _is_json_schema_list(maybe_json_key, maybe_json_value, schema)
        ):
            if not isinstance(maybe_json_value, Mapping):
                return False
            try:
                maybe_sub_schema = get_annotations(schema)[maybe_json_key]
            except KeyError:
                logger.debug("Missing key: %s['%s']", schema, maybe_json_key)
                return False
            # For mappings without annotations, i.e., general mappings, just check if
            # the value is valid JSON
            if not get_annotations(maybe_sub_schema):
                return is_json(maybe_json_value)
            # Otherwise the mapping is a schema, so check if the value conforms
            if not is_json_schema(maybe_json_value, maybe_sub_schema):
                return False
    return True


logger = logging.getLogger(__name__)
if __name__ == "__main__":
    raise SystemExit(0)
