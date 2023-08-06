import re
import builtins
from keyword import iskeyword
from typing import List, Union

from pydantic import parse_obj_as
import openapi_schema_pydantic as oas
from stringcase import snakecase
from . import get_config
from ..source import Source

DELIMITERS = r"\. _-"


def sanitize(value: str) -> str:
    """Replace every character that isn't 0-9, A-Z, a-z, or a known delimiter"""
    return re.sub(rf"[^\w{DELIMITERS}]+", "_", value)


def split_words(value: str) -> List[str]:
    """Split a string on words and known delimiters"""
    # We can't guess words if there is no capital letter
    if any(c.isupper() for c in value):
        value = " ".join(re.split("([A-Z]?[a-z]+)", value))
    return re.findall(rf"[^{DELIMITERS}]+", value)


RESERVED_WORDS = (set(dir(builtins)) | {"self", "true", "false", "datetime"}) - {
    "type",
    "id",
}


def fix_reserved_words(value: str) -> str:
    """
    Using reserved Python words as identifiers in generated code causes problems, so this function renames them.

    Args:
        value: The identifier to-be that should be renamed if it's a reserved word.

    Returns:
        `value` suffixed with `_` if it was a reserved word.
    """
    return f"{value}_" if value in RESERVED_WORDS or iskeyword(value) else value


def snake_case(value: str) -> str:
    """Converts to snake_case"""
    # words = split_words(sanitize(value))
    return snakecase(value)


def pascal_case(value: str) -> str:
    """Converts to PascalCase"""
    words = split_words(sanitize(value))
    return "".join((word if word.isupper() else word.capitalize() for word in words))


def kebab_case(value: str) -> str:
    """Converts to kebab-case"""
    words = split_words(sanitize(value))
    return "-".join(words).lower()


def remove_string_escapes(value: str) -> str:
    return value.replace('"', r"\"")


def concat_snake_name(*names: str) -> str:
    return "_".join(snake_case(name) for name in names)


def build_class_name(name: str) -> str:
    config = get_config()
    class_name = fix_reserved_words(pascal_case(name))
    return config.class_overrides.get(class_name, class_name)


def build_prop_name(name: str) -> str:
    config = get_config()
    name = config.field_overrides.get(name, name)
    return fix_reserved_words(snake_case(name))


def schema_from_source(source: Source) -> oas.Schema:
    data = source.data
    try:
        return parse_obj_as(oas.Schema, data)
    except Exception as e:
        raise TypeError(f"Invalid Schema from {source.uri}") from e
