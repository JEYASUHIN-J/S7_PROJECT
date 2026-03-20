import scrapy
from ..items import NewscrawlerItem
from news.models import Headline
from newscrawler.spiders import news_spider
from newscrawler import pipelines

class NewsSpider(scrapy.Spider):
	name = 'news'
	start_urls=[
		'https://techcrunch.com/'
	]

	def parse(self, response):
		try:
			# Try multiple selector options to find news articles
			div_all_news = response.xpath("//div[@class='river river--homepage']/div[@class='post-block post-block--image post-block--unread']")
			
			# If no results, try a more generic selector
			if not div_all_news:
				div_all_news = response.xpath("//div[contains(@class, 'post-block')]") or \
							  response.xpath("//article") or \
							  response.xpath("//div[contains(@data-type, 'post')]")
				
			i=0
			for some in div_all_news:
				try:
					items = NewscrawlerItem()
					
					# Try to get title with multiple options
					title_elem = some.xpath(".//h2/a/text()").get() or \
								some.xpath(".//h2//text()").get() or \
								some.xpath(".//h3/a/text()").get()
					
					if not title_elem:
						# Try global selectors
						title_selectors = [
							"//header[@class='post-block__header']/h2/a/text()",
							"//div[contains(@class, 'post-block')]/header/h2/a/text()",
							"//article//h2/a/text()"
						]
						
						for selector in title_selectors:
							titles = response.xpath(selector)
							if titles and i < len(titles):
								title_elem = titles[i].extract()
								break
					
					# Try to get link with multiple options
					link_elem = some.xpath(".//h2/a/@href").get() or \
								some.xpath(".//h3/a/@href").get()
					
					if not link_elem:
						# Try global selectors
						link_selectors = [
							"//header[@class='post-block__header']/h2/a/@href",
							"//div[contains(@class, 'post-block')]/header/h2/a/@href",
							"//article//h2/a/@href"
						]
						
						for selector in link_selectors:
							links = response.xpath(selector)
							if links and i < len(links):
								link_elem = links[i].extract()
								break
					
					# Only proceed if we have both title and link
					if title_elem and link_elem:
						# Clean title if needed
						title = title_elem.strip()
						if len(title) > 5:
							title = title[5:-3] if title.startswith('\n') else title
						
						# Get image with multiple options
						img_elem = None
						img_selectors = [
							".//figure//img/@src",
							".//img/@src",
							".//figure//img/@data-src",
							".//img/@data-src",
							".//figure//source/@srcset"
						]
						
						for selector in img_selectors:
							img_elem = some.xpath(selector).get()
							if img_elem:
								break
						
						if not img_elem:
							# Try global selectors
							global_img_selectors = [
								"//footer[@class='post-block__footer']/figure/a/img/@src",
								"//div[contains(@class, 'post-block')]//figure//img/@src",
								"//div[contains(@class, 'post-block')]//img/@src"
							]
							
							for selector in global_img_selectors:
								imgs = response.xpath(selector)
								if imgs and i < len(imgs):
									img_elem = imgs[i].extract()
									break
						
						# Use default image if none found
						if not img_elem or img_elem == '':
							img_elem = "https://techcrunch.com/wp-content/uploads/2022/03/TC-SocialImage-default.jpg"
						
						# Ensure the image URL is absolute
						if img_elem and not img_elem.startswith('http'):
							img_elem = "https:" + img_elem if img_elem.startswith('//') else img_elem
						
						items['title'] = title
						items['image'] = img_elem
						items['url'] = link_elem
						items['source'] = 'Techcrunch'
						yield items
				except Exception as e:
					self.logger.error(f"Error processing technology news item {i}: {str(e)}")
				
				i += 1
		except Exception as e:
			self.logger.error(f"Error in Techcrunch parse method: {str(e)}")

class TechSpider(scrapy.Spider):
	name = 'technews'
	start_urls=[
		'https://www.theverge.com/tech'
	]

	def parse(self, response):
		try:
			# Try to find articles with multiple selectors
			articles = response.xpath("//div[contains(@class, 'duet--content-cards--content-card')]")
			
			# If no results, try alternative selectors
			if not articles:
				articles = response.xpath("//div[contains(@class, 'c-entry-box--compact')]") or \
						  response.xpath("//div[contains(@class, 'c-compact-river')]//div[contains(@class, 'c-entry-box')]") or \
						  response.xpath("//div[contains(@class, 'l-col__main')]//article")
			
			for article in articles:
				try:
					items = NewscrawlerItem()
					
					# Get title with multiple fallbacks
					title_elem = article.xpath(".//h2/a/text()").get() or \
								article.xpath(".//h2//text()").get() or \
								article.xpath(".//h3/a/text()").get()
					
					# Get link with multiple fallbacks
					link_elem = article.xpath(".//h2/a/@href").get() or \
								article.xpath(".//h3/a/@href").get() or \
								article.xpath(".//a/@href").get()
					
					# Skip if we don't have both title and link
					if not title_elem or not link_elem:
						continue
						
					# Clean and process the title
					title = title_elem.strip()
					
					# Process the link
					link = link_elem
					if not link.startswith('http'):
						link = 'https://www.theverge.com' + link
						
					# Get image with multiple fallbacks
					img = None
					img_selectors = [
						".//div[contains(@class, 'duet--content-cards--image')]//img/@src",
						".//div[contains(@class, 'duet--content-cards--image')]//img/@data-src",
						".//div[contains(@class, 'c-entry__image')]//img/@src",
						".//div[contains(@class, 'c-entry__image')]//img/@data-src",
						".//picture//source/@srcset",
						".//picture//source/@data-srcset",
						".//img/@src",
						".//img/@data-src"
					]
					
					for selector in img_selectors:
						img = article.xpath(selector).get()
						if img:
							# Handle srcset (take first source)
							if ',' in img:
								img = img.split(',')[0].strip().split(' ')[0]
							break
					
					# Look for images in style attributes
					if not img:
						try:
							style_attr = article.xpath(".//*[@style]/@style").get()
							if style_attr and "background-image" in style_attr:
								img = style_attr.split("url('")[1].split("')")[0]
						except:
							pass
					
					# Use default image if none found
					if not img or img == '':
						img = "https://cdn.vox-cdn.com/uploads/chorus_asset/file/22319422/theverge.jpg"
					
					# Ensure image URL is absolute
					if img and not img.startswith('http'):
						img = "https:" + img if img.startswith('//') else img
					
					# Only yield if we have all required fields
					if title and link:
						items['title'] = title
						items['image'] = img
						items['url'] = link
						items['source'] = 'The Verge'
						yield items
				except Exception as e:
					self.logger.error(f"Error processing The Verge article: {str(e)}")
		except Exception as e:
			self.logger.error(f"Error in The Verge parse method: {str(e)}")
