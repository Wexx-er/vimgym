"""
Tests for CLI module
"""

from click.testing import CliRunner

from vimgym.cli import cli


def test_cli_help():
    """Test CLI help command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "VimGym - Interactive tutorial for vim" in result.output


def test_hello_command():
    """Test hello command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["hello"])
    assert result.exit_code == 0
    assert "Hello from VimGym!" in result.output


def test_status_command():
    """Test status command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["status"])
    assert result.exit_code == 0
    assert "VimGym v0.1.0" in result.output
    assert "Status: Ready for development" in result.output


def test_version_option():
    """Test version option"""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output
