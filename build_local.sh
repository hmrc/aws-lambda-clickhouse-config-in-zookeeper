#!/usr/bin/env bash

docker run -t -v $(pwd):/data amazonlinux:2.0.20210421.0 /data/package.sh
