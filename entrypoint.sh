#!/bin/sh -l

echo "Spider file $SPIDER_FILE"
# sleep 10

# curl 'http://localhost:8050/render.html?url=https://duckduckgo.com/'

curl 'http://localhost:8050/execute' -H 'Accept: */*' -H 'content-type: application/json' \
-d '{"url":"https://www.cablevisionfibertel.com.ar","wait":0.5,"resource_timeout":0,"viewport":"1024x768","render_all":false,"images":1,"http_method":"GET","html5_media":false,"http2":false,"save_args":[],"load_args":{},"timeout":90,"request_body":false,"response_body":false,"engine":"webkit","har":1,"png":1,"html":1,"lua_source":"function main(splash, args)\r\n  assert(splash:go(args.url))\r\n  assert(splash:wait(1))\r\n\r\n  local locations = splash:evaljs('\''fullLocationsList'\'')\r\n  return { locations=locations }\r\nend"}'

scrapy runspider $SPIDER_FILE

# time=$(date)
# echo "::set-output name=time::$time"
