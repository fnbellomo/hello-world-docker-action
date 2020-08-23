#!/bin/sh -l

echo "Spider file $SPIDER_FILE"
# sleep 10

# curl 'http://localhost:8050/render.html?url=https://duckduckgo.com/'

curl 'http://localhost:8050/execute' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0' -H 'Accept: */*' -H 'Accept-Language: en-US,es-AR;q=0.8,es;q=0.5,en;q=0.3' --compressed -H 'content-type: application/json' -H 'Origin: http://localhost:8050' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Referer: http://localhost:8050/info?wait=0.5&images=1&expand=1&timeout=90.0&url=https%3A%2F%2Fwww.cablevisionfibertel.com.ar&lua_source=function+main%28splash%2C+args%29%0D%0A++assert%28splash%3Ago%28args.url%29%29%0D%0A++assert%28splash%3Await%281%29%29%0D%0A%0D%0A++local+locations+%3D+splash%3Aevaljs%28%27fullLocationsList%27%29%0D%0A++return+%7B+locations%3Dlocations+%7D%0D%0Aend' -H 'Cookie: phaseInterval=120000' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' --data-raw $'{"url":"https://www.cablevisionfibertel.com.ar","wait":0.5,"resource_timeout":0,"viewport":"1024x768","render_all":false,"images":1,"http_method":"GET","html5_media":false,"http2":false,"save_args":[],"load_args":{},"timeout":90,"request_body":false,"response_body":false,"engine":"webkit","har":1,"png":1,"html":1,"lua_source":"function main(splash, args)\\r\\n  assert(splash:go(args.url))\\r\\n  assert(splash:wait(1))\\r\\n\\r\\n  local locations = splash:evaljs(\'fullLocationsList\')\\r\\n  return { locations=locations }\\r\\nend"}''

scrapy runspider $SPIDER_FILE

time=$(date)
echo "::set-output name=time::$time"
