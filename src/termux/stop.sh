#!/bin/bash

for pid in `ps aux | grep 'state\|net-testing'  | grep -v grep | awk '{print $2}'`