#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of log_parser.
# https://github.com/adeelahmad/log_parser

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2022, Adeel Ahmad <230291+adeelahmad@users.noreply.github.com>

from preggy import expect

from log_parser import __version__
from tests.base import TestCase


class VersionTestCase(TestCase):
    def test_has_proper_version(self):
        expect(__version__).to_equal('0.1.0')
