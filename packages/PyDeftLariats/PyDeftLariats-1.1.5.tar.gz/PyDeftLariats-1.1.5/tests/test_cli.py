#!/usr/bin/env python

"""Tests for `src` package."""


import unittest

from click.testing import CliRunner
from deftlariat.entrypoints import cli


class TestSrc(unittest.TestCase):
    """Tests for `src` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        print(result.output)
        assert result.exit_code == 0
        assert 'deft lariats' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
