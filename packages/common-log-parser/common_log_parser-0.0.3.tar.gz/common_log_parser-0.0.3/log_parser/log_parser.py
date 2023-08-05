#!/usr/bin/env python3

import re
from collections import Counter
import ipaddress
import logging

FORMAT = '%(asctime)s -  %(message)s'
logging.basicConfig(format=FORMAT)


class LogParser():

    _file_name: str = ''
    _uniq_ips: dict = {}
    _ip_addr_counter = Counter()
    _url_counter = Counter()
    _urls = {}
    _top_n: int = 3
    _verbose: bool = False
    LOG_REGEX = '^(?P<ip>\S+)\s+-\s*(?P<userid>\S+)\s+\[(?P<datetime>[^\]]+)\]\s+"(?P<method>[a-z]+)\s*(?P<request>[^ "]+)?\s*(http/(?P<http_version>[0-9.]+))?"\s+(?P<status>[0-9]{3})\s+(?P<size>[0-9]+|-).*$'

    def __init__(self, file_name, top_n=3, verbose=False):
        self._file_name = file_name
        self._top_n = int(top_n)
        if verbose is False:
            logging.disable()

    def match_line(self, line):
        pattern = re.compile(self.LOG_REGEX)
        match = pattern.match(line.lower().strip())
        if match and match.group('ip') != '' and match.group('request') != '':
            return match.group('ip'), match.group('request')
        else:
            raise ValueError("Invalid log line: %s" % line)

    def process_data(self, str_ip, request):
        try:
            ip = int(ipaddress.ip_address((str_ip)))
            self._uniq_ips[ip] = str_ip
            self._ip_addr_counter.update([ip])
            hashed_url = hash(request)
            self._url_counter.update([hashed_url])
            self._urls[hashed_url] = request
        except ValueError:
            logging.warning("Invalid IP Address: %s" % str_ip)
            raise ValueError("Invalid IP Address: %s" % str_ip)

    def print_stats(self):
        print(60 * '-')
        print(' << The number of unique IP addresses # %s >>' %
              ("{:,}".format(len(self._urls))))
        print(60 * '-')
        print(' << The top ' + str(self._top_n) +
              ' most visited URLs >>')
        print(60 * '-')
        for i, t in enumerate(self._url_counter.most_common(self._top_n)):
            print('%2d) %6s: %s visits' %
                  (i + 1, self._urls[t[0]], "{:,}".format(t[1])))
        print(60 * '-')

        print(' << The top ' + str(self._top_n) +
              ' most active IP addresses >>')
        print(60 * '-')
        for i, t in enumerate(self._ip_addr_counter.most_common(self._top_n)):
            print('%2d) %6s: %s visits' %
                  (i + 1, ipaddress.ip_address(t[0]), "{:,}".format(t[1])))
        print(60 * '-')

    def parse(self):
        self.parse_log_file()
        self.print_stats()

    def parse_log_file(self):

        # f = open(self._file_name, 'r+')
        try:
            with open(self._file_name) as f:
                line_no = 0
                for line in f:
                    # Find the path which is after the GET and surrounded by spaces.
                    line_no += 1
                    try:
                        str_ip, request = self.match_line(line)
                        try:
                            self.process_data(str_ip, request)
                        except ValueError:
                            logging.warning("Invalid log data: %s" %
                                            self._file_name + ":%s" % line_no)
                            pass
                    except ValueError:
                        logging.warning("Invalid log line: %s" % self._file_name +
                                        ":%s" % line_no)
                        pass
        except FileNotFoundError:
            logging.error("File not found: %s" % self._file_name)
            raise ValueError("File not found: %s" % self._file_name)
