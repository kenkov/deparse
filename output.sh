#! /bin/sh
# coding:utf-8

python output_dot.py | tee dottest.dot && dot -Tpng dottest.dot -o dottest.png
