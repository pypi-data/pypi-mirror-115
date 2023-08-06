"""A wrapper around the click library that makes its CLI components callable as functions"""

import click

from collections import OrderedDict

from .version import __version__


_CLICK_OBJECT_CREATORS = [
    click.option, click.argument, click.group, click.command, click.password_option, 
    click.confirmation_option, click.version_option, click.help_option,
]


def _create_click_object(arg_name, click_params):
    """
    Creates a ``click`` object that can be applied in an argument stack using the configurations in 
    ``click_params``.

    The following keys of ``click_params`` are used by ``callable_cli``:

    * ``arg_type`` is a callable from the ``click`` library that creates an argument class that can 
      be added to a ``click`` argument stack. Defaults to ``click.option``.
    * ``flags`` is a list of command-line flags for this option; if this is present, ``arg_type`` 
      must be set to ``click.option``

    All other keys are passed as keyword arguments to the callable set as ``arg_type``.

    If the argument type is ``click.option`` (the default) and no flags are specified, the flags 
    defaults to ``[f"--{arg_name}".replace("_", "-")]``.
    """
    arg_type = click_params.pop("arg_type", click.option)
    if arg_type not in _CLICK_OBJECT_CREATORS:
        raise ValueError(f"Received invalid arg_type {arg_type}")
        # TODO: add a more helpful error message if click.Option, click.Command, etc. passed

    # construct the flags if this is an option
    if arg_type == click.option:
        default_flag = f"--{arg_name}".replace("_", "-")
        flags = click_params.pop("flags", [default_flag])
        if len(flags) == 0:
            flags.append(default_flag)  # add the default flag if a user specifies an empty list

        # don't allow invalid command-line flags
        for flag in flags:
            if flag[0] != "-":
                raise ValueError(f"Argument {arg_name} has an invalid flag: {flag}")

    # otherwise, there are no flags
    else:
        if "flags" in click_params:
            raise ValueError("The 'flags' key can only be specified with click.option as the " \
                             "argument type")
        flags = []

    # include the arg_name as the last element to make sure click routes it to the correct kwarg
    flags.append(arg_name)

    return arg_type(*flags, **click_params)


def create_group(*args, **kwargs):
    """
    An alias for ``click.group``.
    """
    return click.group(*args, **kwargs)


def create_command(group, prog, args, **kwargs):
    """
    Creates a command within the click group ``group`` with command name ``prog``. The command-line
    arguments are parsed from the dictionary ``args``. Keyword arguments in ``kwargs`` are passed to
    ``group.command``.
    """
    args = OrderedDict(args)
    args_to_defaults = OrderedDict(**{arg: args.get("default") for arg in args})

    def verify_args_and_call(f, **kwargs):
        """
        A wrapper around a function ``f`` that takes in any keyword arguments, ensures that they are
        valid by comparing them to the args declared in ``create_command``, loads the default values
        for any missing arguments, and returns the value of calling ``f`` on those arguments.
        """
        for kw in kwargs:
            if kw not in args:
                raise TypeError(f"{f.__name__}() received unexpected argument '{kw}'")

        # load default argument values
        new_kwargs = args_to_defaults.copy()
        new_kwargs.update(kwargs)

        # call the wrapped function
        return f(**new_kwargs)

    def create_click_command_and_wrapper(f):
        """
        A wrapper around a function ``f`` that creates a ``click`` command-line interface using the
        arguments and keyword arguments declared in ``args``. Registers the function as a command
        in the group ``group`` and returns a wrapper function that can be called like the original
        function, *but with all argument names specified*.
        """
        click_f = f
        for arg in list(args.keys())[::-1]:
            click_params = args[arg]
            click_f = _create_click_object(arg, click_params)(click_f)

        # register the command with the group
        click_f = group.command(prog, **kwargs)(click_f)

        # TODO: render a more informative error than what currently happens:
        # TypeError: call_function() takes 0 positional arguments but 4 were given
        def call_function(**kwargs):
            """
            A wrapper that takes in a series of keyword arguments can calls the wrapped function
            using ``verify_args_and_call`` to verify the arguments and load the defaults.
            """
            return verify_args_and_call(f, **kwargs)

        # update the function name
        call_function.__name__ = f.__name__

        return call_function

    return create_click_command_and_wrapper
