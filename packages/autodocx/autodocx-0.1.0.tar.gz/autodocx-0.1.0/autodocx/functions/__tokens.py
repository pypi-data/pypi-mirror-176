import re

from typing import Callable, List, Tuple, Union, Any

DOT = "."


def extract_tokens(body: str) -> List[str]:
    body = str(body)

    variablesx = re.compile("\{\{([^\{\}]*)\}\}", re.M)
    variables: List[str] = variablesx.findall(body)
    variables = [v.lower() for v in variables]

    return variables


def replace_tokens(resolved_tokens: List[Tuple[List[str], str]], body: str) -> str:
    processed_body = body

    for resolved_token in resolved_tokens:
        variable = str(resolved_token[0])
        value = str(resolved_token[1])

        replacex = re.compile("\{\{%s\}\}" % variable, re.IGNORECASE)

        processed_body = re.sub(replacex, value.replace("\\", "\\\\"), processed_body)

    return processed_body


def get_value_if_key_exists(*keys, map: dict, else_return_value="") -> Any:
    if not isinstance(map, dict):
        return else_return_value
    if len(keys) == 0:
        raise AttributeError(
            "__get_value_if_key_exists() expects at least two arguments, one given."
        )

    _element = map
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return else_return_value

    return _element


def bind(
    original: str,
    repl_map: dict[str, Union[str, Callable[[], str]]],
) -> str:
    if not isinstance(original, str):
        raise ValueError(f"{original.__class__.__name__} is not str")

    if not isinstance(repl_map, dict):
        raise ValueError(f"{repl_map.__class__.__name__} is not dict")
    tokens = extract_tokens(body=original)

    resolved_tokens = []
    for token in tokens:
        value = get_value_if_key_exists(token, map=repl_map, else_return_value="")

        if callable(value):
            value = value()

        value = str(value)

        resolved_tokens.append([token, value])

    return replace_tokens(resolved_tokens=resolved_tokens, body=original)
