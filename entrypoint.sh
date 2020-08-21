#!/bin/sh -l

echo "Spider file $1"

scrapy runspider $1

time=$(date)
echo "::set-output name=time::$time"
