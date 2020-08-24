import json
import hashlib
from pathlib import Path, PurePath
from shutil import copyfile
from datetime import datetime

import pandas as pd
# from influxdb import InfluxDBClient
from scrapy.exporters import CsvItemExporter
from scrapy.statscollectors import StatsCollector

# import influx_config as config


class ToCsvPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.spider.custom_settings

        spider_name = crawler.spider.name
        proyect=settings.get('BOT_NAME', spider_name)
        output_dir = settings.get('OUTPUT_DIR', './')
        file_path = PurePath(output_dir, proyect, f'{spider_name}.csv')

        return cls(
            file_path=file_path,
            header=settings['CSV']['HEADER'],
            sort_by=settings['CSV']['SORT_BY'],
        )

    def __init__(self, file_path, header, sort_by):
        self.sort_by = sort_by
        self.file_path = file_path

        # Create the output file
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        self.file = open(file_path, 'ab')

        if (Path(file_path).stat().st_size == 0):
            self.file.write(str.encode(','.join(header) + '\n'))

        self.exporter = CsvItemExporter(self.file, include_headers_line=False)
        self.exporter.fields_to_export = header
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

        df = pd.read_csv(self.file_path)
        df = df.drop_duplicates()

        if self.sort_by:
            df = df.sort_values(by=self.sort_by, ascending=True)

        df.to_csv(self.file_path, index=False)

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class DataPackagedPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings

        return cls(
            spider_name=crawler.spider.name,
            output_dir=settings.get('OUTPUT_DIR'),
            proyect=settings.get('BOT_NAME')
        )

    def __init__(self, spider_name, output_dir, proyect):
        self.spider_name = spider_name
        self.datapackage_path = f'{output_dir}/{proyect}/datapackage.json'
        self.output_file_path = f'{output_dir}/{proyect}/{spider_name}.csv'

        if not os.path.isfile(self.datapackage_path):
            copyfile('./datapackage.json', self.datapackage_path)

    def close_spider(self, spider):
        name = f'smn_{self.spider_name}'

        with open(self.datapackage_path) as file:
            datapackage = json.load(file)

        for i, resource in enumerate(datapackage['resources']):
            if resource['name'] == name:
                break

        md5sum = hashlib.md5(open(self.output_file_path,'r').read().encode()).hexdigest()

        datapackage['resources'][i]['hash'] = md5sum
        datapackage['resources'][i]['bytes'] = os.path.getsize(self.output_file_path)
        datapackage['resources'][i]['last_updated'] = datetime.now().isoformat()

        with open(self.datapackage_path, 'w') as file:
            json.dump(datapackage, file, indent=2, ensure_ascii=False)

    def process_item(self, item, spider):
        return item


class InfluxDbPipeline(object):
    def __init__(self):
        self.cnt = 0
        self.client = InfluxDBClient(host=config.host, port=config.port, database=config.database)
        self.client.create_database(config.database)

    def process_item(self, item, spider):
        self.cnt += 1

        if self.cnt % 500 == 0:
            stats = spider.crawler.stats
            time = datetime.utcnow().isoformat()

            measurements = [{
                'measurement': 'spiders',
                'tags': {
                    'spider_name': spider.name
                },
                'time': time + 'Z',
                'fields': {
                    'request_bytes': stats.get_value('downloader/request_bytes', 0),
                    'request_count': stats.get_value('downloader/request_count', 0),
                    'response_bytes': stats.get_value('downloader/response_bytes', 0),
                    'response_count': stats.get_value('downloader/response_count', 0),
                    'response_status_count_200': stats.get_value('downloader/response_status_count/200', 0),
                    'response_status_count_201': stats.get_value('downloader/response_status_count/201', 0),
                    'response_status_count_202': stats.get_value('downloader/response_status_count/202', 0),
                    'response_status_count_400': stats.get_value('downloader/response_status_count/400', 0),
                    'response_status_count_401': stats.get_value('downloader/response_status_count/401', 0),
                    'response_status_count_403': stats.get_value('downloader/response_status_count/403', 0),
                    'response_status_count_404': stats.get_value('downloader/response_status_count/404', 0),

                    'log_count_info': stats.get_value('log_count/INFO', 0),
                    'log_count_debug': stats.get_value('log_count/DEBUG', 0),
                    'log_count_error': stats.get_value('log_count/ERROR', 0),

                    'item_scraped_count': stats.get_value('item_scraped_count', 0),
                    'item_dropped_count': stats.get_value('item_dropped_count', 0)
                }
            }]

            self.client.write_points(measurements)
            print(stats.get_stats())

        return item
