#!/usr/bin/python

from collections import namedtuple
import os

TestStruct = namedtuple('TestStruct', 'name run expect timeout before after')


class TestParser():
    @staticmethod
    def read_all():
        test_suite = []
        for root, dirs, files in os.walk('./runtime'):
            for filename in files:
                test_suite.append(TestParser.read(root + '/' + filename))
        return test_suite

    @staticmethod
    def read(file_name):
        file = open(file_name, 'r')
        tests = []

        test_lines = []
        for line in file.readlines():
            if line != '\n':
                test_lines.append(line)
            else:
                tests.append(TestParser.__read_test_struct(test_lines))
                test_lines = []
        tests.append(TestParser.__read_test_struct(test_lines))

        file.close()
        return (file_name.split('/')[2], tests)

    @staticmethod
    def __read_test_struct(test):
        name = ''
        run = ''
        expect = ''
        timeout = ''
        before = ''
        after = ''

        for item in test:
            item_split = item.split()
            item_name = item_split[0]
            line = ' '.join(item_split[1:])

            if item_name == 'NAME':
                name = line
            elif item_name == 'RUN':
                run = line
            elif item_name == 'EXPECT':
                expect = line
            elif item_name == 'TIMEOUT':
                timeout = int(line.strip(' '))
            elif item_name == 'BEFORE':
                before = line
            elif item_name == 'AFTER':
                after = line

        return TestStruct(name, run, expect, timeout, before, after)
