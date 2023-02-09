import scrapy


class WixySpider(scrapy.Spider):
    name = "wixy"
    allowed_domains = ["www.jumia.co.ke"]
    start_urls = ["https://www.jumia.co.ke/smartphones/"]

    def parse(self, response):
        for item in response.css('article.prd._fb.col.c-prd'):
            yield{
                'name': item.css('h3.name::text').get(),
                'link': item.css('a.core').attrib['href'] ,
                'price': item.css('div.prc::text').get(),
                'oldprice':item.css('div.old::text').get(),
                'stars':item.css('div.stars._s::text').get(),
                'percentage discount':item.css('div.bdg._dsct._sm::text').get()
            }
            
        next = response.xpath("//a[contains(@aria-label,'Next Page')]").attrib['href']
        
        if next is not None:
            nextpage = response.urljoin(next)
            yield response.follow(nextpage,callback = self.parse)