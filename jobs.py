import scrapy
from scrapy import Request


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ["peopleperhour.com"]
    start_urls = ['https://www.peopleperhour.com/freelance-jobs']

    
    def parse(self, response):
        links = response.css('[class="title"] a::attr(href)').extract()
        i = 0
        for link in links:
            titles = response.css('[class="title"] a::attr(title)').extract()[i]
            titles_link = response.css('[class="title"] a::attr(href)').extract()[i]
            published_date = response.css('[class="crop value"] ::attr(title)').extract()[i]
            #etiquette_orange = response.css('[class="etiquette orange"]').extract()[i]

            relative_url = link
            absolute_url = response.urljoin(relative_url)
            i = i + 1
            yield scrapy.Request(absolute_url, callback=self.parse_target_page, meta={
                'page': response.url,  
                'titles_link': titles_link,
                'titles': titles,
                'published_date': published_date,
                #'etiquette_orange': etiquette_orange 
                })

        next_page = response.css('[class="next"]::attr(href)').extract_first()
        absolute_next_url = 'https://www.peopleperhour.com' + next_page
        #if next_page:
        #    yield scrapy.Request(absolute_next_url, callback=self.parse)        
        yield scrapy.Request(absolute_next_url, callback=self.parse)


    def parse_target_page(self, response):
        page = response.meta.get('page')
        titles = response.meta.get('titles')
        titles_link = response.meta.get('titles_link')
        published_date = response.meta.get('published_date')
        #etiquette_orange = response.meta.get('etqiuette_orange')
        
        ## New features are been added other than description from each of the links 
        start_url = "https://www.peopleperhour.com/freelance-jobs/"
        categories_collected = titles_link.replace(start_url, '').split('/')
        job_category = categories_collected[0]
        job_sub_category = categories_collected[1]
        posted_time = response.css('[class="info-value"]::text').extract()[0]
        proposal_sent_count = response.css('[class="info-value"]::text').extract()[1]
        proposal_like_count = response.css('[class=" count-stars"]::text').extract()[0]
        location = response.css('[class="info-label"]::text').extract()[3]
        etiquette_blue = response.css('[class="etiquette blue"]::text').extract()
        etiquette_yellow = response.css('[class="etiquette yellow"]::text').extract()
        open_for_proposal = response.css('[class="info-label job-status open-for-proposals"]::text').extract()
        experience_level = response.css('[class="description-experience-level"]::text').extract()[1]
        end_in_days = response.css('[class="value"]::text').extract()[0]
        proposal_price_rate = response.css('[class="discreet"]::text').extract()[1]
        proposal_price = response.css('[class="value price-tag"]::text').extract()[0] \
                       + response.css('[class="value price-tag"] span::text').extract()[0]
        description = "".join(line for line in response.css('[class="project-description gutter-top"]::text').extract())
        yield {
                'page': page,
                'titles_link': titles_link,
                'titles':titles,
                'job_category': job_category,
                'job_sub_category': job_sub_category,
                'published_date': published_date,                 
                'posted_time': posted_time, 
                'proposal_sent_count': proposal_sent_count,
                'proposal_like_count': proposal_like_count,
                'location': location,
                'etiquette_blue': etiquette_blue,
                'etiquette_yellow': etiquette_yellow,
                #'etiquette_orange': etiquette_orange,
                'open_for_proposal': open_for_proposal,
                'experience_level': experience_level,
                'end_in_days': end_in_days, 
                'proposal_price_rate': proposal_price_rate,
                'proposal_price': proposal_price,                
                'description': description
                } 
