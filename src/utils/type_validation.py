import typing


def find_type_origin(type_hint: type):
    if isinstance(type_hint, typing._SpecialForm):
        # case of typing.Any, typing.ClassVar, typing.Final, typing.Literal,
        # typing.NoReturn, typing.Optional, or typing.Union without parameters
        return

    actual_type = typing.get_origin(
        type_hint) or type_hint  # requires Python 3.8
    if isinstance(actual_type, typing._SpecialForm):
        # case of typing.Union[…] or typing.ClassVar[…] or …
        for origins in map(find_type_origin, typing.get_args(type_hint)):
            yield from origins
    else:
        yield actual_type


def check_types(parameters: typing.Mapping, hints: typing.Mapping):
    for name, value in parameters.items():
        type_hint = hints.get(name, typing.Any)
        actual_types = tuple(find_type_origin(type_hint))
        if actual_types and not isinstance(value, actual_types):
            raise TypeError(
                f"Expected type '{type_hint}' for argument '{name}'"
                f" but received type '{type(value)}' instead.")
