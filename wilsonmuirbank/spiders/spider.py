import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import WwilsonmuirbankItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class WwilsonmuirbankSpider(scrapy.Spider):
	name = 'wilsonmuirbank'
	start_urls = ['http://www.whyitsmybank.com/blog']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall() + response.xpath('//div[@class="articleTitle-sidebar"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@class="article-date"]/b/text()').get()
		title = response.xpath('//h2/a/text()').get()
		content = response.xpath('//div[@class="article-body"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=WwilsonmuirbankItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
