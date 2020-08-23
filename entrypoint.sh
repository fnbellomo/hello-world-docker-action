#!/bin/sh -l

echo "Spider file $SPIDER_FILE"
sleep 10

curl 'http://localhost:8050/render.html?url=https://duckduckgo.com/'

scrapy runspider $SPIDER_FILE

time=$(date)
echo "::set-output name=time::$time"
