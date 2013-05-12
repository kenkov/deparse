#! /usr/bin/env python
# coding:utf-8

from __future__ import division
import deparse
import sys

if __name__ == '__main__':
    #import sys
    s = sys.stdin.readline().strip()
    parser = deparse.Parser(s, '--charset=UTF8')
    labels = {}

    print "digraph G {"
    print "  graph [rankdir = BT]"
    for chunk in parser:
        _id = chunk.id if chunk.id != -1 else "root"
        arrow = u'  n{} -> n{}'.format(
            _id,
            chunk.link if chunk.link != -1 else "root")
        print arrow
        label = []
        for token in chunk:
            label.append(token.surface)
        labels[_id] = " ".join(label)
    for i, v in labels.items():
        fmt = u'  n{} [label="{}", fontname="Ricty"]'
        print fmt.format(i, v).encode('utf-8')
    print u'  nroot [label="root"]'.format(i, v).encode('utf-8')
    print "}"
