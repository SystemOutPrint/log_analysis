# -*- coding:utf-8 -*-

import re
import sys
import time


class LogCountEntry:
    def __init__(self):
        self.size = 0L
        self.row = 0


if __name__ == '__main__':
    date = sys.argv[1]
    input_file_name = sys.argv[2]
    output_file_name = sys.argv[3]
    key_idx = int(sys.argv[4])

    old = time.clock()
    print "count开始"
    key = ""
    count = {}
    input_file = open(input_file_name, 'r')
    for row in input_file:
        all_match = re.split('\s+', row, key_idx + 1)
        if all_match[0] == date:
            key = all_match[key_idx]
        log_count_entry = count.get(key, LogCountEntry())
        log_count_entry.size += sys.getsizeof(row)
        log_count_entry.row += 1
        count[key] = log_count_entry
    print 'count结束，耗时%s' % (time.clock() - old)

    output_file = open(output_file_name, 'w+')
    old = time.clock()
    print "sort开始"
    sorted_count = sorted(count.items(), key=lambda x: x[1].size, reverse=True)
    print 'sort结束，耗时(%s)' % (time.clock() - old)
    for key, value in sorted_count:
        print >> output_file, '{key}: {size}字节, {row}行'.format(key=key, size=value.size, row=value.row)