import pickle
from scrapy import Spider
from scrapy.http import Request

class FlipkartSpider(Spider):
    name = 'flipkart'
    start_urls = ['https://www.flipkart.com/search?q=Laptop']
    all_data =[]
    number = 100
    def parse(self, response):
        laptops = response.css("div._3O0U0u")
        flag=True
        for laptop in laptops:
            name = laptop.css('div._3wU53n::text').get()
            price = laptop.css('div._1vC4OE::text').get()
            rating = laptop.css('div.hGSR34::text').get()
            data = {'name': name, 'price': price, 'rating': rating}
            self.all_data.append(data)
            yield data
            if len(self.all_data) <= self.number:
                pass
            else:
                flag=False
                break



        # list of relative urls (previous and next)
        next_page= response.css('a._3fVaIS::attr(href)').getall()
        if next_page and flag:
            next_page_url = response.urljoin(next_page[-1]) # pick the "next" url
            self.log(f'relative url: {next_page_url}')
            yield Request(next_page_url, callback=self.parse)
        pickle.dump(self.all_data,(open("pickle.data","wb")))
