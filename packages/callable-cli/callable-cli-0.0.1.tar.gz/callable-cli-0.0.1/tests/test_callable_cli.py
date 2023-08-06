"""Tests for the callable_cli package"""

import callable_cli
import click
import pytest

from click.testing import CliRunner
from unittest import mock


CLI_RUNNER = CliRunner()


def test__create_click_object():
    """
    Tests for ``callable_cli._create_click_object``.
    """
    examples = [
        (("foo", {}), ["--foo", "foo"]),
        (("foo", {"flags": []}), ["--foo", "foo"]),
        (("bar", {
            "help": "does bar",
            "arg_type": mock.MagicMock(),
        }), ["bar"]),
    ]

    for i, (args, expected_flags) in enumerate(examples):
        try:
            click_params = args[1]
            arg_type = click_params.get("arg_type")
            with mock.patch("callable_cli.click") as mocked_click:
                # make sure we don't get a validation error for the arg_type
                callable_cli._CLICK_OBJECT_CREATORS.append(mocked_click.option)
                if arg_type:
                    callable_cli._CLICK_OBJECT_CREATORS.append(arg_type)

                out = callable_cli._create_click_object(*args)

                # remove the mock
                callable_cli._CLICK_OBJECT_CREATORS.remove(mocked_click.option)
                if arg_type:
                    callable_cli._CLICK_OBJECT_CREATORS.remove(arg_type)

                for key in ["flags", "arg_type"]:
                    args[1].pop(key, None)

                # check that the decorator was correctly instantiated
                if arg_type:
                    assert out == arg_type.return_value
                    arg_type.assert_called_once_with(*expected_flags, **click_params)
                    mocked_click.option.assert_not_called()
                else:
                    assert out == mocked_click.option.return_value
                    mocked_click.option.assert_called_once_with(*expected_flags, **args[1])

        # inform the user which iteration caused the error
        except:
            print(f"Error occurred at itertion {i}")
            raise

    # test invalid arg_type error
    with pytest.raises(ValueError, match=r"Received invalid arg_type .*"):
        callable_cli._create_click_object("foo", {
            "arg_type": 1,
        })

    # test click class error with hint
    with pytest.raises(ValueError, match=r"Received invalid arg_type .*"):
        callable_cli._create_click_object("foo", {
            "arg_type": click.Option,
        })

    # test invalid flags
    with pytest.raises(ValueError, match=r"Argument \w+ has an invalid flag: [\w-]+"):
        callable_cli._create_click_object("foo", {
            "flags": ["--bar", "baz"],
        })

    # test flags present for non-option argument
    with pytest.raises(
        ValueError, 
        match="The 'flags' key can only be specified with click.option as the argument type",
    ):
        callable_cli._create_click_object("foo", {
            "arg_type": click.argument,
            "flags": ["--bar", "baz"],
        })



def test_create_group(capsys):
    """
    Tests for ``callable_cli.create_group``.
    """
    @callable_cli.create_group()
    @callable_cli.click.version_option(version="0.0.1")
    def cli():
        """
        This is the CLI.
        """
        pass

    assert isinstance(cli, click.Group)

    result = CLI_RUNNER.invoke(cli, ["--version"], prog_name="foo")
    assert result.exit_code == 0
    assert result.stdout == "foo, version 0.0.1\n"


def test_create_command(capsys):
    """
    Tests for ``callable_cli.create_command``.
    """
    @callable_cli.create_group()
    def cli():
        """
        This is the CLI.
        """
        pass

    @callable_cli.create_command(cli, "cmd", {
        "foo": {
            "flags": ["-f", "--foo"],
            "help": "does foo",
            "default": None,
            "type": callable_cli.click.STRING,
        },
        "bar": {
            "flags": ["-b"],
            "help": "does bar",
            "default": 1,
            "type": callable_cli.click.INT,
        },
        "baz": {
            "help": "does baz",
            "type": callable_cli.click.Path(),
            "required": True,
        },
        "qux": {
            "arg_type": callable_cli.click.argument,
            "type": callable_cli.click.Path(exists=True),
        },
    })
    def do_something(foo, bar, baz, qux):
        """
        This is the docstring for do_something()
        """
        print(foo)
        print(bar)
        print(baz)
        print(qux)

    @callable_cli.create_command(cli, "other-cmd", {
        "quuz": {
            "flags": ["-q"],
            "is_flag": True,
        }
    })
    def do_something_else(quuz):
        """
        This is the docstring for do_something_else()
        """
        if quuz:
            print(quuz)

    # check that __name__ was set
    assert do_something.__name__ == "do_something"

    do_something(foo=1, bar=2, baz=3, qux=4)

    # check that everything was printed correctly
    captured = capsys.readouterr()
    assert captured.out.strip() == "1\n2\n3\n4"

    # check that calling with an invalid argument throws an error
    with pytest.raises(TypeError, match=r"do_something\(\) received unexpected argument 'quux'"):
        do_something(quux=1)

    result = CLI_RUNNER.invoke(cli, ["cmd", "--baz", "./foo", "./tests"])
    assert result.exit_code == 0
    assert result.stdout == "None\n1\n./foo\n./tests\n"

    result = CLI_RUNNER.invoke(cli, ["other-cmd"])
    assert result.exit_code == 0
    assert result.stdout == ""

    result = CLI_RUNNER.invoke(cli, ["other-cmd", "-q"])
    assert result.exit_code == 0
    assert result.stdout == "True\n"

    # test CLI with a qux that does not exist
    result = CLI_RUNNER.invoke(cli, ["cmd", "-f", "100", "--baz", "..", "./does-not-exist.txt"])
    assert result.exit_code != 0
    assert "Invalid value for 'QUX': Path './does-not-exist.txt' does not exist." in result.stdout
