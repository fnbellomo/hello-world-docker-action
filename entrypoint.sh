#!/bin/sh -l

echo "Spider file $1"
sleep 10

curl 'http://localhost:8050/render.html?url=https://duckduckgo.com/'

scrapy runspider $1

time=$(date)
echo "::set-output name=time::$time"
