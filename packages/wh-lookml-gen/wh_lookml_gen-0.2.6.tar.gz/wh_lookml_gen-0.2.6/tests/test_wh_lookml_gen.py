#!/usr/bin/env python

"""Tests for `wh_lookml_gen` package."""


import unittest
from click.testing import CliRunner

from wh_lookml_gen import wh_lookml_gen
from wh_lookml_gen import cli


class TestWh_lookml_gen(unittest.TestCase):
    """Tests for `wh_lookml_gen` package."""

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
        assert result.exit_code == 0
        assert 'wh_lookml_gen.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
