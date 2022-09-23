"""Test cmdline"""
from __future__ import annotations  # PEP 585

import pytest
from click.testing import CliRunner

from python_project import __version__
from python_project.cmdline import main


@pytest.mark.parametrize(
    ['invoke_args', 'exit_code', 'output_keyword'],
    [
        ([], 0, 'help'),
        (['--help'], 0, 'help'),
        (['--version'], 0, __version__),
        (['-V'], 0, __version__),
        (['--debug', '--verbose', 'run'], 0, 'run'),
    ]
)
def test_main(
        clicker: CliRunner,
        invoke_args: list[str],
        exit_code: int,
        output_keyword: str,
):
    """Test main cmdline"""
    result = clicker.invoke(main, invoke_args)
    assert result.exit_code == exit_code
    assert output_keyword in result.output


"""Test cmdline"""
import sys

import pytest

from python_project import cmdline


def test_help(mocker, capsys):
    """test help command"""
    args = ['word_count', '-h']
    mocker.patch.object(sys, 'argv', args)
    with pytest.raises(SystemExit) as ex:
        cmdline.main()

    assert ex.value.code == 0
    outerr = capsys.readouterr()
    assert '-s SOURCE' in outerr.out
    assert '-d DEST' in outerr.out

def test_only_pass_source(mocker, capsys):
    """test only pass -s """
    args = ['word_count', '-s', 'foo']
    mocker.patch.object(sys, 'argv', args)
    with pytest.raises(SystemExit) as ex:
        cmdline.main()

    assert ex.value.code == 2
    outerr = capsys.readouterr()
    assert 'the following arguments are required: -d' in outerr.err

def test_only_pass_dest(mocker, capsys):
    """test only pass -d"""
    args = ['word_count', '-d', 'foo']
    mocker.patch.object(sys, 'argv', args)
    with pytest.raises(SystemExit) as ex:
        cmdline.main()

    assert ex.value.code == 2
    outerr = capsys.readouterr()
    assert 'the following arguments are required: -s' in outerr.err

def test_main(mocker):
    """test cmdline, and everything is fine."""
    args = ['word_count', '-s', 'foo', '-d', 'bar']
    mocker.patch.object(sys, 'argv', args)
    mock_count = mocker.patch('python_project.cmdline.count')
    cmdline.main()
    mock_count.assert_called_once()

