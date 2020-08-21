#!/bin/sh -l

echo "Spider file $1"

# cp $1 ./baseSpider/baseSpider/spiders/
# cd baseSpider
# scrapy crawl $2
scrapy runspider $1

time=$(date)
echo "::set-output name=time::$time"
