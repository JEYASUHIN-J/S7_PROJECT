import scrapy
from ..items import EconomycrawlerItem
from news.models import EHeadline
from economycrawler.spiders import economy_spider
from economycrawler import pipelines

class EconomySpider(scrapy.Spider):
	name = "economy"
	start_urls = [
		'https://economictimes.indiatimes.com/markets/stocks/news'
	]

	def parse(self, response):
		div_all_news = response.xpath("//div[@class='eachStory']")
		i=0
		for some in div_all_news:
			try:
				items = EconomycrawlerItem()
				
				# Try to get title with error handling
				title_elem = some.xpath(".//h3/a/text()").get() or some.xpath(".//h3/a/meta/@content").get()
				if not title_elem:
					title_elem = response.xpath("//h3/a/meta/@content")[i].extract() if i < len(response.xpath("//h3/a/meta/@content")) else None
				
				# Try to get link with error handling
				link_elem = some.xpath(".//h3/a/@href").get()
				if not link_elem:
					link_elem = response.xpath("//h3/a/@href")[i].extract() if i < len(response.xpath("//h3/a/@href")) else None
				
				# Only proceed if we have a title and link
				if title_elem and link_elem:
					link = "https://economictimes.indiatimes.com" + link_elem if not link_elem.startswith('http') else link_elem
					
					# Enhanced image extraction with multiple selectors and attributes
					img = None
					# Try direct image selectors first
					img_selectors = [
						".//a/span[@class='imgContainer']/img/@data-original",
						".//a/span[@class='imgContainer']/img/@src",
						".//a/span[@class='imgContainer']/img/@data-src",
						".//a/span[@class='imgContainer']/img/@lazy-src",
						".//a//img/@src",
						".//a//img/@data-src",
						".//img/@src",
						".//img/@data-src"
					]
					
					for selector in img_selectors:
						img = some.xpath(selector).get()
						if img:
							break
					
					# If no image found, try global selectors
					if not img:
						global_selectors = [
							"//a/span[@class='imgContainer']/img/@data-original",
							"//a/span[@class='imgContainer']/img/@src",
							"//a/span[@class='imgContainer']/img/@data-src"
						]
						
						for selector in global_selectors:
							img_elements = response.xpath(selector)
							if i < len(img_elements):
								img = img_elements[i].extract()
								break
					
					# If still no image, use a default news image
					if not img or img == "":
						img = "https://img.etimg.com/thumb/width-640,height-360,imgsize-76282,resizemode-1,msid-72074484/news/economy/policy/the-economic-times.jpg"
					
					# Make sure image URL is absolute
					if img and not img.startswith('http'):
						img = "https:" + img if img.startswith('//') else "https://economictimes.indiatimes.com" + img
					
					items["title"] = title_elem
					items["image"] = img
					items["url"] = link
					items['source'] = 'Economic Times'
					yield items
			except Exception as e:
				self.logger.error(f"Error processing item {i}: {str(e)}")
				
			i += 1

class ExpressSpider(scrapy.Spider):
	name = "express"
	start_urls = [
		'https://indianexpress.com/section/business/economy/'
	]

	def parse(self, response):
		div_all_news = response.xpath("//div[@class='articles']")
		i=0
		for some in div_all_news:
			try:
				items = EconomycrawlerItem()
				
				# Try to get title with error handling
				title_elem = some.xpath(".//h2/a/text()").get()
				if not title_elem:
					title_elem = response.xpath("//h2/a/text()")[i].extract() if i < len(response.xpath("//h2/a/text()")) else None
				
				# Try to get link with error handling
				link_elem = some.xpath(".//h2/a/@href").get() 
				if not link_elem:
					link_elem = response.xpath("//h2/a/@href")[i].extract() if i < len(response.xpath("//h2/a/@href")) else None
				
				# Only proceed if we have a title and link
				if title_elem and link_elem:
					# Enhanced image extraction with multiple methods
					img_elem = None
					
					# Method 1: Try direct image selectors
					img_selectors = [
						".//div/a/img/@src",
						".//div/a/img/@data-src",
						".//div[@class='snaps']/a/img/@src",
						".//div[@class='snaps']/a/img/@data-src",
						".//img/@src",
						".//img/@data-src"
					]
					
					for selector in img_selectors:
						img_elem = some.xpath(selector).get()
						if img_elem:
							break
							
					# Method 2: Try noscript extraction
					if not img_elem:
						try:
							img_container = some.xpath(".//div/a/noscript").get() or response.xpath("//div/a/noscript")[i].extract()
							if img_container:
								if 'src="' in img_container:
									img_elem = img_container.split('src="')[1].split('"')[0]
								else:
									l = img_container.split('"')
									img_elem = l[5] if len(l) > 5 else ""
						except:
							pass
							
					# Method 3: Try global selectors
					if not img_elem:
						global_selectors = [
							"//div[@class='articles']//div/a/img/@src",
							"//div[@class='articles']//div/a/img/@data-src"
						]
						
						for selector in global_selectors:
							img_elements = response.xpath(selector)
							if i < len(img_elements):
								img_elem = img_elements[i].extract()
								break
					
					# Method 4: Extract from style attribute if available
					if not img_elem:
						try:
							style_attr = some.xpath(".//div[@class='snaps']//div/@style").get()
							if style_attr and "background-image" in style_attr:
								img_elem = style_attr.split("url('")[1].split("')")[0]
						except:
							pass
					
					# If still no image found, use a default image
					if not img_elem or img_elem == "":
						img_elem = "https://images.indianexpress.com/2021/02/indian-express-logo.jpg"
					
					# Make sure image URL is absolute
					if img_elem and not img_elem.startswith('http'):
						img_elem = "https:" + img_elem if img_elem.startswith('//') else img_elem
					
					items["title"] = title_elem
					items["image"] = img_elem
					items["url"] = link_elem
					items["source"] = 'Indian Express'
					yield items
			except Exception as e:
				self.logger.error(f"Error processing item {i}: {str(e)}")
				
			i += 1