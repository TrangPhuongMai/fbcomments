# -*- coding: utf-8 -*-
import scrapy
import logging
import pandas as pd
from scrapy.http import Request


class FbcSpider(scrapy.Spider):
    name = 'fbc'
    urls = pd.read_csv('/home/nero/PycharmProjects/fbpost/mbasic.csv')
    # start_urls = urls['URL'][:30].array
#     start_urls = ['https://mbasic.facebook.com/100008351743433_2059052677716437',
#     'https://mbasic.facebook.com/100001066815770_2782341571811376',
#     'https://mbasic.facebook.com/100013579247666_850744192054881',
    start_urls = ['https://mbasic.facebook.com/story.php?story_fbid=2323944954503899&id=100006652505738&_rdr']
    # start_urls = ['https://mbasic.facebook.com/']

    def __init__(self, *args, **kwargs):
        self.cookies = {
            'xs': '29%3AlKjif7UZZ_0U5Q%3A2%3A1576776002%3A15834%3A7574',
            'c_user': '100041490302112',
            'datr': 'tDLpXat5uwGulyERUfE4tvbb',
            'fr': '1euulrl7ka6mguy4M.AWVQhO_ufRQW-9dMu2bv8oLSkGE.Bddc7a.6q.F4H.0.0.BeEjvL.AWUSbfCB'
        }

    def parse(self, response):
        for url in self.start_urls:
            yield Request(url, cookies=self.cookies, meta={ 'proxy': "http://103.143.206.17:443"},
                          callback=self.parse_p)

    def parse_p (self,response):
        # logging.info('================== {} =================='.format(response.xpath("//*[contains(@id,'sentence')]/following-sibling::div//text()")))
        # comments_block = response.xpath("//*[contains(@id,'sentence')]/following-sibling::div")
        # get all replied comments
        comments_block = response.xpath(
            ".//div[string-length(@class) = 2 and count(@id)=1 and contains('0123456789', substring(@id,1,1)) and .//div[contains(@id,'comment_replies')]]//a[contains(@href,'comment/replies/')]/@href").extract()
        path = './/div[string-length(@class) = 2 and count(@id)=1 and contains("0123456789", substring(@id,1,1)) and .//div[contains(@id,"comment_replies")]]' + '[' + str(
            1) + ']'

        for reply in response.xpath(path):
            source = reply.xpath('.//h3/a/text()').extract()
            source_url = reply.xpath('.//h3/a/@href').get()
            answer = reply.xpath('.//a[contains(@href,"repl")]/@href').extract()
            ans = response.urljoin(answer[::-1][0])
            logging.info('================== {} ==========source \n'.format(source))
            logging.info('================== {} ==========nested replied \n'.format(ans))
            logging.info('================== {} ==========owner of the nested replied ROOT\n'.format(source_url))



            return Request(url=ans,callback=self.parse_replied)



    def parse_replied (sell,response):

        logging.info('================== {} ========== nested comments content'.format(response.xpath('//div//text()').extract()))

        logging.info(response)
        return




