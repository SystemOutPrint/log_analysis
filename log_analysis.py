# -*- coding:utf-8 -*-

import re
import sys
import time


class LogCountEntry:
    def __init__(self):
        self.size = 0L
        self.row = 0
        self.avg_size = 0


if __name__ == '__main__':
    log_start = sys.argv[1]
    input_file_name = sys.argv[2]
    output_file_name = sys.argv[3]
    key_idx = int(sys.argv[4])

    key = ""  # 统计key值，根据key_idx解析，目前只支持空格分隔
    count = {}  # 统计map，key是统计key值，value是LogCountEntry
    input_file = open(input_file_name, 'r')

    print "count开始"
    old = time.clock()
    for row in input_file:
        # 根据log_start解析本行key值，如果遇到pretty json这种带有换行符的日志，采用上次解析成功的key值统计
        all_match = re.split('\s+', row, key_idx + 1)
        if all_match[0] == log_start:
            key = all_match[key_idx]

        # 逐行统计
        log_count_entry = count.get(key, LogCountEntry())
        log_count_entry.size += sys.getsizeof(row)
        log_count_entry.row += 1
        count[key] = log_count_entry
    print 'count结束，耗时%s' % (time.clock() - old)
    input_file.close()

    old = time.clock()
    print "sort开始"
    sorted_count = sorted(count.items(), key=lambda x: int(x[1].size / x[1].row), reverse=True)
    print 'sort结束，耗时(%s)' % (time.clock() - old)

    print "开始输出统计结果"
    output_file = open(output_file_name, 'w+')
    for key, value in sorted_count:
        print >> output_file, '{key}: {size}字节, {row}行, {avg}' \
            .format(key=key, size=value.size, row=value.row, avg=int(value.size / value.row))
    output_file.close()
    print "结束输出统计结果"
