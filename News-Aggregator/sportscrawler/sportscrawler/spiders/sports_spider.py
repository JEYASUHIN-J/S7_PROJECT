import scrapy
from ..items import SportscrawlerItem
from news.models import SHeadline
from sportscrawler.spiders import sports_spider
from sportscrawler import pipelines

class SportsSpider(scrapy.Spider):
	name = "sports"
	start_urls = [
		'https://indianexpress.com/section/sports/'
	]

	def parse(self, response):
		div_all_news = response.xpath("//div[@class='articles']")
		i=0
		for some in div_all_news:
			try:
				items = SportscrawlerItem()
				
				# Try to get title with error handling
				title_elem = some.xpath(".//h2[@class='title']/a/text()").get()
				if not title_elem:
					title_elem = response.xpath("//h2[@class='title']/a/text()")[i].extract() if i < len(response.xpath("//h2[@class='title']/a/text()")) else None
				
				# Try to get link with error handling
				link_elem = some.xpath(".//h2[@class='title']/a/@href").get()
				if not link_elem:
					link_elem = response.xpath("//h2[@class='title']/a/@href")[i].extract() if i < len(response.xpath("//h2[@class='title']/a/@href")) else None
				
				# Only proceed if we have a title and link
				if title_elem and link_elem:
					# Enhanced image extraction with multiple methods
					img_elem = None
					
					# Method 1: Try direct image selectors
					img_selectors = [
						".//div[@class='snaps']/a/img/@src",
						".//div[@class='snaps']/a/img/@data-src",
						".//div/a/img/@src",
						".//div/a/img/@data-src",
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
							img_container = some.xpath(".//div[@class='snaps']/a/noscript").get() or response.xpath("//div[@class='snaps']/a/noscript")[i].extract()
							if img_container:
								if 'src="' in img_container:
									img_elem = img_container.split('src="')[1].split('"')[0]
								else:
									l = img_container.split(" ")
									img_elem = l[3][5:-1] if len(l) > 3 else ""
						except:
							pass
							
					# Method 3: Try global selectors
					if not img_elem:
						global_selectors = [
							"//div[@class='articles']//div[@class='snaps']/a/img/@src",
							"//div[@class='articles']//div[@class='snaps']/a/img/@data-src"
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
					
					# If still no image, use a default sports image
					if not img_elem or img_elem == "":
						img_elem = "https://images.indianexpress.com/2019/04/sports.jpg"
					
					# Make sure image URL is absolute
					if img_elem and not img_elem.startswith('http'):
						img_elem = "https:" + img_elem if img_elem.startswith('//') else img_elem
						
					items["title"] = title_elem
					items["image"] = img_elem
					items["url"] = link_elem
					items['source'] = 'Indian Express'
					yield items
			except Exception as e:
				self.logger.error(f"Error processing item {i}: {str(e)}")
				
			i += 1

class HtimesSpider(scrapy.Spider):
	name = "Htimes"
	start_urls = [
		'https://www.hindustantimes.com/other-sports/'
	]

	def parse(self, response):
		try:
			# Try different selector paths to adapt to site changes
			div_all_news = response.xpath("//section[@class='container']/div[@class='news-area more-news-section']/div/div[@class='col-sm-7 col-md-8 col-lg-9']/div[@id='scroll-container']/ul[@class='latest-news-morenews more-latest-news more-separate newslist-sec']/li/div")
			
			# If no results, try a more generic selector
			if not div_all_news:
				div_all_news = response.xpath("//ul[contains(@class, 'latest-news-morenews')]/li/div")
				
			i=0
			j=0
			for some in div_all_news:
				try:
					items = SportscrawlerItem()
					
					# Try several options for title
					title_elem = some.xpath(".//div[@class='media-body']/div/a/text()").get()
					if not title_elem:
						title_elem = response.xpath("//div[@class='media-body']/div/a/text()")[i].extract() if i < len(response.xpath("//div[@class='media-body']/div/a/text()")) else None
					
					# If still no title, try alternative selectors
					if not title_elem:
						title_elem = some.xpath(".//div[contains(@class, 'media-body')]//a/text()").get()
						
					# Try several options for link
					link_elem = some.xpath(".//div[@class='media-body']/div/a/@href").get()
					if not link_elem:
						link_elem = response.xpath("//div[@class='media-body']/div/a/@href")[i].extract() if i < len(response.xpath("//div[@class='media-body']/div/a/@href")) else None
					
					# If still no link, try alternative selectors
					if not link_elem:
						link_elem = some.xpath(".//div[contains(@class, 'media-body')]//a/@href").get()
					
					# Only proceed if we have a title and link
					if title_elem and link_elem:
						# Enhanced image extraction with multiple fallbacks
						img_elem = None
						
						# Method 1: Try position-specific selectors
						try:
							if i < 3:
								img_elem = some.xpath(".//div[@class='media-left']/div/a/img/@src").get() or \
										  some.xpath(".//div[@class='media-left']/div/a/img/@data-src").get()
								if not img_elem and i < len(response.xpath("//div[@class='media-left']/div/a/img/@src")):
									img_elem = response.xpath("//div[@class='media-left']/div/a/img/@src")[i].extract()
							else:
								img_elem = some.xpath(".//div[@class='media-left']/a/img/@src").get() or \
										  some.xpath(".//div[@class='media-left']/a/img/@data-src").get()
								if not img_elem and j < len(response.xpath("//div[@class='media-left']/a/img/@src")):
									img_elem = response.xpath("//div[@class='media-left']/a/img/@src")[j].extract()
						except:
							pass
							
						# Method 2: Try generic image selectors
						if not img_elem:
							img_selectors = [
								".//img/@src",
								".//img/@data-src",
								".//div[contains(@class, 'media-left')]//img/@src",
								".//div[contains(@class, 'media-left')]//img/@data-src"
							]
							
							for selector in img_selectors:
								img_elem = some.xpath(selector).get()
								if img_elem:
									break
						
						# Method 3: Look for lazy-loaded images
						if not img_elem:
							lazy_selectors = [
								".//img/@data-lazy-src",
								".//img/@lazy-src",
								".//img/@data-lazy"
							]
							
							for selector in lazy_selectors:
								img_elem = some.xpath(selector).get()
								if img_elem:
									break
									
						# Method 4: Extract from style attribute
						if not img_elem:
							try:
								style_attr = some.xpath(".//*[@style]/@style").get()
								if style_attr and "background-image" in style_attr:
									img_elem = style_attr.split("url('")[1].split("')")[0]
							except:
								pass
						
						# If still no image, use a default news image
						if not img_elem or img_elem == "":
							img_elem = "https://www.hindustantimes.com/images/app-images/ht-logo.svg"
							
						# Make sure image URL is absolute
						if img_elem and not img_elem.startswith('http'):
							img_elem = "https:" + img_elem if img_elem.startswith('//') else img_elem
							
						items["title"] = title_elem
						items["image"] = img_elem
						items["url"] = link_elem
						items['source'] = 'Hindustan'
						yield items
				except Exception as e:
					self.logger.error(f"Error processing item {i}: {str(e)}")
					
				i += 1
				if i > 0 and j <= i:
					j += 1
		except Exception as e:
			self.logger.error(f"Error in parse method: {str(e)}")
