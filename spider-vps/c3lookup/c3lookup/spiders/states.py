# -*- coding: utf-8 -*-
import scrapy


class StatesSpider(scrapy.Spider):
    name = 'states'
    allowed_domains = ['501c3lookup.org']
    start_urls = ['http://501c3lookup.org/Washington/']

    def parse(self, response):

        base_url='http://501c3lookup.org'        
        links=response.xpath('//*[@id="post"]/div/table/tr/td/a/@href').extract()

        for link in links:
            absurl=base_url+link
            yield scrapy.Request(absurl,callback=self.parse_charity)

        
        # NextPage
        l=response.xpath('//*[@id="next_bot"]/@href').extract_first()
        next_page_link='http://501c3lookup.org/Washington/'+l
        yield scrapy.Request(next_page_link,callback=self.parse)
        # pg_1090


    def parse_charity(self,response):
        
        name=response.xpath('//*[@itemprop="name"]/text()').extract_first()
        
        # Address
        temp=response.xpath('//*[@itemprop="address"]/span/text()').extract()
        city=temp[0]
        state='Washington'

        address=''
        for val in temp[1:]:
            address=address+" "+val.strip()
        
        ein=response.xpath('//*[@class="col-md-10"]/h3/span/text()').extract_first().strip()
        try:
            category=response.xpath('//*[@class="col-md-10"]/h3/span/text()').extract()[1].strip()
            if(category==''):
                category=response.xpath('//*[@class="col-md-10"]/h3/span/a/text()').extract_first().strip()
        except:
            category=''


        # Social Media
        selector=response.xpath('//*[@class="col-md-6 501c3_data"]/h5')

        tele=selector[2].xpath('.//span/text()').extract_first().strip()
        url=selector[3].xpath('.//@href').extract_first()
        facebook=selector[5].xpath('.//@href').extract_first()
        twitter=selector[7].xpath('.//@href').extract_first()


        # print (name)
        # # print(city)
        # # print(ein)
        # # print(category)
        # # print(address)
        # print(tele)
        # print(url)
        # print(facebook)
        # print(twitter)


        yield { 'Name' : name,
                'EIN'  : ein,
                'Category': category,
                'Telephone': tele,
                'Address':address,
                'City': city,
                'State': state,
                'Website': url,
                'Facebook': facebook,
                'Twitter': twitter
            }

