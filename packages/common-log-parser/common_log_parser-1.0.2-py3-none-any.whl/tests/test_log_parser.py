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
from log_parser import LogParser
from testfixtures import TempDirectory


class LogParserTestCase(TestCase):

    def test_log_parser_parse_with_single_log(self):
        d = TempDirectory()
        d.write(
            'sample_log', b'240.234.133.207 - - [01/Nov/2022:13:42:14 +1100] "POST /aggregate HTTP/1.1" 502 29298')
        log_parser = LogParser(d.path+"/sample_log")
        log_parser.parse()
        # expect(log_parser.uniq_ips).to_length(1)
        # expect(log_parser.ip_addr_counter).to_length(1)
        expect(log_parser.urls).to_length(1)
        d.cleanup()

    def test_log_parser_parse_with_many_logs(self):
        tempd = TempDirectory()
        tempd.write('sample_log_2', bytes("""44.144.216.165 - stracke3216 [01/Nov/2022:14:42:47 +1100] "PUT /whiteboard HTTP/1.1" 400 5556
44.144.216.165 - sporer2678 [01/Nov/2022:14:42:47 +1100] "PUT /back-end/dynamic HTTP/2.0" 401 7310
44.144.216.165 - - [01/Nov/2022:14:42:47 +1100] "HEAD /open-source/best-of-breed/e-tailers HTTP/2.0" 100 2292
44.144.216.165 - - [01/Nov/2022:14:42:47 +1100] "PUT /markets/systems HTTP/1.1" 400 15215
44.144.216.165 - von4038 [01/Nov/2022:14:42:47 +1100] "PUT /web+services/frictionless/experiences HTTP/2.0" 200 3716
69.168.104.169 - jacobs6557 [01/Nov/2022:14:42:47 +1100] "POST /extend/portals/world-class/collaborative HTTP/2.0" 416 19830
69.168.104.169 - - [01/Nov/2022:14:42:47 +1100] "POST /engage/revolutionary HTTP/2.0" 203 4649
69.168.104.169 - - [01/Nov/2022:14:42:47 +1100] "HEAD /intuitive/24%2f365 HTTP/2.0" 204 26129
69.168.104.169 - - [01/Nov/2022:14:42:47 +1100] "GET /synthesize HTTP/2.0" 200 7794
69.168.104.169 - mohr2327 [01/Nov/2022:14:42:47 +1100] "PATCH /infrastructures/bandwidth HTTP/2.0" 301 20733
185.7.152.93 - - [01/Nov/2022:14:42:47 +1100] "DELETE /benchmark/drive/functionalities/dynamic HTTP/2.0" 403 27760
25.222.195.23 - - [01/Nov/2022:14:42:47 +1100] "HEAD /initiatives/niches HTTP/2.0" 203 13122
25.222.195.23 - fisher1620 [01/Nov/2022:14:42:47 +1100] "PUT /envisioneer/engage HTTP/2.0" 401 8804
25.222.195.23 - mclaughlin7610 [01/Nov/2022:14:42:47 +1100] "PUT /bricks-and-clicks HTTP/1.0" 201 7861
25.222.195.23 - blanda5420 [01/Nov/2022:14:42:47 +1100] "POST /recontextualize/killer/transform/strategic HTTP/1.1" 404 3460""", 'utf-8'))
        log_parser_2 = LogParser(tempd.path+"/sample_log_2")
        log_parser_2.parse()
        # expect(log_parser_2.uniq_ips).to_length(4)
        # expect(log_parser_2.ip_addr_counter).to_length(4)
        # tempd.cleanup()

    @classmethod
    def tearDownClass(cls):
        TempDirectory.cleanup_all()
