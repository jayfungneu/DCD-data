import scrapy
from dcd.items import DcdItem

class DcdcommentsSpider(scrapy.Spider):
    name = "dcdcomments"
    allowed_domains = ["dongchedi.com"]
    start_urls = ["https://www.dongchedi.com/community/145/cardrive"]
    def __init__(self):
        self.initrow=1
        self.end=139
    def parse(self, response):
        comment_lists=response.xpath('''//*[@id="__next"]/div[1]/div[2]/div[3]/div[2]/div[3]/section''')
        end_page=response.xpath('//*[@id="__next"]/div[1]/div[2]/div[3]/div[2]/div[4]/ul/li[7]/a/span/text()').extract_first()
        for comment_list in comment_lists:
            temp=DcdItem()
            temp['user_name']=comment_list.xpath('./div[1]/div/a/div/div[2]/div/p/span[1]/text()').extract_first()
            temp['user_comment']=comment_list.xpath('./div[2]/p/a/span/text()').extract_first()
            temp['using_age']=comment_list.xpath('./div[1]/div/a/div/div[2]/div[2]/span/text()').extract_first()
            if temp['user_comment'] ==None:
                temp['user_title']=comment_list.xpath('./div[2]/a/h3/text()').extract_first()
                get_more_info=comment_list.xpath('./div/p/a[2]/span[2]/text()').extract_first()
                if(get_more_info!=None):
                    detail_url='https://www.dongchedi.com'+comment_list.xpath('./div/p/a[2]/@href').extract_first()
                    yield scrapy.Request(detail_url, callback=self.more_details, meta={"item": temp})
            else:
                temp['user_title']=None
                yield temp


        # 翻页
        self.initrow = self.initrow + 1

        if self.initrow <= self.end:
            next_url = "https://www.dongchedi.com/community/145/cardrive"+'-'+str(self.initrow)
            yield scrapy.Request(url=next_url, callback=self.parse)

    def more_details(self,response):
        data = response.meta['item']
        node_list=response.xpath('//*[@id="__next"]/div/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div/p')
        comment=''


        for node in node_list:
            content=node.xpath('./text()').extract_first()
            if content !=None:
                comment=comment+content+','

        data['user_comment']=comment

        yield data

