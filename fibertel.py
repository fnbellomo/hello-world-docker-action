import json
from datetime import datetime

import scrapy
from scrapy_splash import SplashRequest

class FibertelItem(scrapy.Item):
    fecha = scrapy.Field()
    provincia = scrapy.Field()
    ciudad = scrapy.Field()
    velocidad = scrapy.Field()
    precio = scrapy.Field()


class FibertelSpider(scrapy.Spider):
    name = 'fibertel'

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        }
    }

    def start_requests(self):
        script = """
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(1))

            local locations = splash:evaljs('fullLocationsList')
            return { locations=locations }
        end
        """

        url = 'https://www.cablevisionfibertel.com.ar'

        yield SplashRequest(url, self.get_all_location,
            endpoint='execute',
            args={'lua_source': script}
        )

    def get_all_location(self, response):
        script = """
        function main(splash, args)
            splash:set_viewport_size(1980, 1020)

            assert(splash:go(args.url))
            assert(splash:wait(0.5))

            splash:runjs([[
                const ev = document.createEvent('Events')
                ev.initEvent('keypress', true, true)
                ev.keyCode = 13
                ev.which = 13
                ev.charCode = 13
                ev.key = 'Enter'
                ev.code = 'Enter'

                const input = document.getElementById('localidad-input')
                input.value = '{location}'
                input.dispatchEvent(ev)
            ]])

            assert(splash:wait(10))

            return {{
                html = splash:html()
            }}
        end
        """

        url_template = 'https://www.cablevisionfibertel.com.ar/internet/fibertel-{speed}-megas'
        locations = json.loads(response.body)['locations']

        # for speed in [50, 100, 300]:
        for speed in [50]:
            for location in locations[:20]:
                yield SplashRequest(
                    url_template.format(speed=speed),
                    self.parse,
                    dont_filter=True,
                    endpoint='execute',
                    args={'lua_source': script.format(location=location)},
                    cb_kwargs={'location': location, 'speed': speed}
                )

    def parse(self, response, location, speed):
        state, city = location.split(',', maxsplit=1)
        price = response.xpath("//span[contains(@class, 'side-box-price ')]/text()").get()
        if price:
            price = ' '.join(price.replace('.', '').split())

        item = FibertelItem()
        item['fecha'] = datetime.now().strftime('%Y-%m-%d')
        item['provincia'] = state
        item['ciudad'] = city
        item['velocidad'] = speed
        item['precio'] = price

        yield item
