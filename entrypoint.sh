#!/bin/sh -l

echo "Hello $1"

scrapy crawl quotes

time=$(date)
echo "::set-output name=time::$time"
