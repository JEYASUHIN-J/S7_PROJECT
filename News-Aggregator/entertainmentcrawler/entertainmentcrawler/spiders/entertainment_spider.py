import scrapy
from ..items import EntertainmentcrawlerItem
from news.models import ENHeadline
from entertainmentcrawler.spiders import entertainment_spider
from entertainmentcrawler import pipelines

class EntertainmentSpider(scrapy.Spider):
	name = "entertainment"
	start_urls = [
		'https://variety.com/'
	]

	def parse(self, response):
		try:
			# Get articles with proper error handling
			articles = response.xpath("//div[@class='l-river__content']/ul/li/article")
			
			# If no articles found, try alternative selectors
			if not articles:
				articles = response.xpath("//div[contains(@class, 'l-river__content')]//article") or \
						  response.xpath("//ul[contains(@class, 'c-features__listitem')]//article")
			
			for i, article in enumerate(articles):
				try:
					items = EntertainmentcrawlerItem()
					
					# Try to get title with multiple selector options
					title_elem = article.xpath(".//header/h3/a/text()").get() or \
								article.xpath(".//h3/a/text()").get() or \
								article.xpath(".//a[contains(@class, 'c-title')]/text()").get()
					
					# Fallback if direct approach fails
					if not title_elem and i < len(response.xpath("//div[@class='l-river__content']/ul/li/article/header/h3/a/text()")):
						title_elem = response.xpath("//div[@class='l-river__content']/ul/li/article/header/h3/a/text()")[i].extract()
					
					# Try to get link with multiple selector options
					link_elem = article.xpath(".//figure/a/@href").get() or \
								article.xpath(".//a[contains(@class, 'c-title')]/@href").get() or \
								article.xpath(".//header//a/@href").get()
					
					# Fallback if direct approach fails
					if not link_elem and i < len(response.xpath("//div[@class='l-river__content']/ul/li/article/figure/a/@href")):
						link_elem = response.xpath("//div[@class='l-river__content']/ul/li/article/figure/a/@href")[i].extract()
					
					# Only proceed if we have a title and link
					if title_elem and link_elem:
						# Enhanced image extraction with multiple methods
						img_elem = None
						
						# Method 1: Try various image selectors
						img_selectors = [
							".//figure//img/@data-src",
							".//figure//img/@src",
							".//img/@data-src",
							".//img/@src",
							".//picture/source/@data-srcset",
							".//picture/img/@data-src",
							".//div[contains(@class, 'c-lazy-image')]//img/@src",
							".//div[contains(@class, 'c-lazy-image')]//img/@data-src"
						]
						
						for selector in img_selectors:
							img_elem = article.xpath(selector).get()
							if img_elem:
								# If it's a comma-separated list (srcset), take the first one
								if "," in img_elem:
									img_elem = img_elem.split(",")[0].strip().split(" ")[0]
								break
						
						# Method 2: Check for background image in style attributes
						if not img_elem:
							try:
								style_attr = article.xpath(".//*[@style]/@style").get()
								if style_attr and "background-image" in style_attr:
									img_elem = style_attr.split("url('")[1].split("')")[0]
							except:
								pass
						
						# Method 3: Use original fallbacks for consistent behavior
						if not img_elem and i < len(response.xpath("//div[@class='l-river__content']/ul/li/article/figure/a/img/@data-src")):
							img_elem = response.xpath("//div[@class='l-river__content']/ul/li/article/figure/a/img/@data-src")[i].extract()
						
						# If still no image, use a default entertainment image
						if not img_elem or img_elem == "":
							img_elem = "https://variety.com/wp-content/themes/vmc/images/variety-logo.svg"
						
						# Make sure image URL is absolute
						if img_elem and not img_elem.startswith('http'):
							img_elem = "https:" + img_elem if img_elem.startswith('//') else img_elem
						
						items["title"] = title_elem
						items["image"] = img_elem
						items["url"] = link_elem
						items['source'] = 'Variety'
						yield items
						
					# Stop after 13 items or if we've processed all found articles
					if i >= 12 or i >= len(articles)-1:
						break
				except Exception as e:
					self.logger.error(f"Error processing entertainment article {i}: {str(e)}")
		except Exception as e:
			self.logger.error(f"Error in Entertainment parse method: {str(e)}")

class EntrtnmentSpider(scrapy.Spider):
	name = "entrtnment"
	start_urls = [
		'https://indianexpress.com/section/entertainment/'
	]

	def parse(self, response):
		try:
			# Try multiple selector paths to find articles
			articles = response.xpath("//div[@class='nation']/div[@class='articles']") or \
					  response.xpath("//div[contains(@class, 'articles')]")
			
			for i in range(min(17, len(articles))):
				try:
					items = EntertainmentcrawlerItem()
					
					# Try to get title with error handling
					title_elem = None
					title_selectors = [
						"//div[@class='nation']/div[@class='articles']/div[@class='title']/a/text()",
						"//div[contains(@class, 'articles')]/div[@class='title']/a/text()",
						"//div[contains(@class, 'articles')]//h2/a/text()"
					]
					
					for selector in title_selectors:
						title_matches = response.xpath(selector)
						if title_matches and i < len(title_matches):
							title_elem = title_matches[i].extract()
							break
							
					# Try to get link with error handling
					link_elem = None
					link_selectors = [
						"//div[@class='nation']/div[@class='articles']/div[@class='snaps']/a/@href",
						"//div[contains(@class, 'articles')]/div[@class='snaps']/a/@href",
						"//div[contains(@class, 'articles')]//h2/a/@href"
					]
					
					for selector in link_selectors:
						link_matches = response.xpath(selector)
						if link_matches and i < len(link_matches):
							link_elem = link_matches[i].extract()
							break
					
					# Only proceed if we have a title and link
					if title_elem and link_elem:
						# Enhanced image extraction
						img_elem = None
						
						# Method 1: Try direct image selectors
						img_selectors = [
							"//div[@class='articles'][{}]//img/@src".format(i+1),
							"//div[@class='articles'][{}]//img/@data-src".format(i+1)
						]
						
						for selector in img_selectors:
							img_matches = response.xpath(selector)
							if img_matches:
								img_elem = img_matches[0].extract()
								break
								
						# Method 2: Try noscript extraction
						if not img_elem:
							img_selectors = [
								"//div[@class='nation']/div[@class='articles']/div[@class='snaps']/a/noscript",
								"//div[contains(@class, 'articles')]/div[@class='snaps']/a/noscript"
							]
							
							for selector in img_selectors:
								img_matches = response.xpath(selector)
								if img_matches and i < len(img_matches):
									s = img_matches[i].extract()
									try:
										if 'src="' in s:
											img_elem = s.split('src="')[1].split('"')[0]
										else:
											l = s.split('"')
											img_elem = l[5] if len(l) > 5 else ""
									except:
										pass
									break
						
						# Method 3: Find image in style attribute
						if not img_elem:
							try:
								style_selectors = [
									"//div[@class='nation']/div[@class='articles'][{}]/div[@class='snaps']//div/@style".format(i+1),
									"//div[contains(@class, 'articles')][{}]//*[@style]/@style".format(i+1)
								]
								
								for selector in style_selectors:
									style_attr = response.xpath(selector).get()
									if style_attr and "background-image" in style_attr:
										img_elem = style_attr.split("url('")[1].split("')")[0]
										break
							except:
								pass
						
						# If still no image, use default entertainment image
						if not img_elem or img_elem == "":
							img_elem = "https://images.indianexpress.com/2019/12/entertainment-1.jpg"
						
						# Make sure image URL is absolute
						if img_elem and not img_elem.startswith('http'):
							img_elem = "https:" + img_elem if img_elem.startswith('//') else img_elem
						
						items["title"] = title_elem
						items["image"] = img_elem
						items["url"] = link_elem
						items["source"] = 'Indian Express'
						yield items
				except Exception as e:
					self.logger.error(f"Error processing entertainment article {i}: {str(e)}")
		except Exception as e:
			self.logger.error(f"Error in Entertainment-Indian Express parse method: {str(e)}")