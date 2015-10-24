#!/usr/bin/env bash

sudo lrun --max-cpu-time 1 --max-real-time 1 --max-memory 512m --network false --isolate-process true --uid 23333 --gid 23333 $@
