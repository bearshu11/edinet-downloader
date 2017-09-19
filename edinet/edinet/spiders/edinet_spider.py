import scrapy
from scrapy.selector import Selector


class EdinetSpider(scrapy.Spider):
    name = "edinet"

    def start_requests(self):
        urls = [
            'http://resource.ufocatch.com/atom/edinetx/query/6094',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.body)
        xml = Selector(response)
        xml.register_namespace('ns','http://www.w3.org/2005/Atom')
        titles = xml.xpath('//ns:entry/ns:title/text()').extract()
        links = xml.xpath('//ns:entry/ns:link[@type="application/zip"]/@href').extract()
        quartery_reports = []
        annual_reports = []
        extra_reports = []
        other_reports = []
        for (title, link) in zip(titles, links):
            if '四半期報告書' in title:
                quartery_reports.append({title:link})
            elif '有価証券報告書' in title:
                annual_reports.append({title:link})
            elif '臨時報告書' in title:
                extra_reports.append({title:link})
            else:
                other_reports.append({title:link})
        print(quartery_reports)
        print(annual_reports)
        print(extra_reports)

        # print(links)
        # for (title, link) in zip(titles, links):
        #     print(title, link)
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
