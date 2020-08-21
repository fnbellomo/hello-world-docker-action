#!/bin/sh -l

echo "Spider path $1"
echo "Spider name $2"

cp $1 ./baseSpider/baseSpider/spiders/
cd baseSpider
scrapy crawl $2

time=$(date)
echo "::set-output name=time::$time"
