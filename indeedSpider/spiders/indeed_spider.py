import re
import json
import scrapy
from urllib.parse import urlencode

class IndeedJobSpider(scrapy.Spider):
    name = "indeed_jobs"
    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv',}}
        }

    def get_indeed_search_url(self, keyword = None, location = None, job_type=None, offset=0):
        parameters = {}
        if keyword:
            parameters["q"] = keyword
        if location:
            parameters["l"] = location
        if job_type:
            parameters["sc"] = job_type
        parameters["filter"] = 0
        parameters["start"] = offset
        return "https://ca.indeed.com/jobs?" + urlencode(parameters)
# https://ca.indeed.com/jobs?q=part+time&l=Alberta&from=searchOnHP&vjk=76c1452456efa959
# https://ca.indeed.com/jobs?q=part+time&l=Alberta&sc=0kf%3Ajt%28parttime%29%3B&vjk=76c1452456efa959

    def start_requests(self):
        # keyword_list = []
        location_list = ['Alberta']
        job_type = "0kf:jt(parttime)"
        for location in location_list:
            indeed_jobs_url = self.get_indeed_search_url(keyword=None, location=location, job_type=job_type)
            yield scrapy.Request(url=indeed_jobs_url, callback=self.parse_search_results, meta={'location': location, 'offset': 0})

    def parse_search_results(self, response):
        location = response.meta['location']
        # keyword = response.meta['keyword'] 
        offset = response.meta['offset'] 
        print("**************Offset is :" + str(offset) + "*****************")
        script_tag  = re.findall(r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});', response.text)
        if script_tag is not None:
            json_blob = json.loads(script_tag[0])
             # Paginate Through Jobs Pages
            
            ## Extract Jobs From Search Page
            jobs_list = json_blob['metaData']['mosaicProviderJobCardsModel']['results']
            for index, job in enumerate(jobs_list):
                if job.get('jobkey') is not None:
                    job_url = 'https://ca.indeed.com/m/basecamp/viewjob?viewtype=embedded&jk=' + job.get('jobkey')
                    yield scrapy.Request(url=job_url, 
                            callback=self.parse_job, 
                            meta={
                                # 'keyword': keyword, 
                                'location': location, 
                                'job_name': job.get('displayTitle', 'N/A'),
                                'page': round(offset / 10) + 1 if offset > 0 else 1,
                                'position': index,
                                'jobKey': job.get('jobkey'),
                                'salary': job.get('salarySnippet').get('text') if job.get('salarySnippet') is not None else '',
                                'company': job.get('company'),
                                'job location': job.get('formattedLocation'),
                                'relativeTime': job.get('formattedRelativeTime'),
                                'jobDescription': job.get('snippet') if job.get('snippet') is not None else '',
                            })
            # if offset == 0:
            #     # meta_data = json_blob["metaData"]["mosaicProviderJobCardsModel"]["tierSummaries"]
            #     meta_data = json_blob["metaData"]["mosaicProviderJobCardsModel"]["tierSummaries"]
            #     # meta_data = json_blob["metaData"]["mosaicProviderJobCardsModel"]
            #     # num_results = sum(category["jobCount"] for category in meta_data)
            #     num_results = 0
            #     print("**************meta_data:", meta_data)
            #     for index, category in enumerate(meta_data):
            #         # print(f"Processing category {index}: {category}")
            #         num_results += category.get("jobCount", 0)
            #     print("**************Number of Results is :" + str(num_results) + "*****************")
            #     if num_results > 100:
            #         num_results = 100
            num_results = 200
            for offset in range(10, num_results + 10, 10):
                url = self.get_indeed_search_url(keyword=None, location=location, offset=offset)
                yield scrapy.Request(url=url, callback=self.parse_search_results, meta={'location': location, 'offset': offset})
            
    def parse_job(self, response):
        location = response.meta['location']
        # keyword = response.meta['keyword'] 
        page = response.meta['page'] 
        position = response.meta['position'] 
        jobName = response.meta['job_name']
        salary = response.meta['salary']
        company = response.meta['company']
        jobLocation = response.meta['job location']
        relativeTime = response.meta['relativeTime']
        jobDescription = response.meta['jobDescription']
        script_tag  = re.findall(r"_initialData=(\{.+?\});", response.text)
        if script_tag is not None:
            json_blob = json.loads(script_tag[0])
            job = json_blob["jobInfoWrapperModel"]["jobInfoModel"]["jobInfoHeaderModel"]
            yield {
                # 'keyword': keyword,
                'location': location,
                'page': page,
                'company': company,
                'jobName': jobName,
                'salary': salary,
                'position': position,
                'job location': jobLocation,
                'relativeTime': relativeTime,
                'jobkey': response.meta['jobKey'],
                'jobDescription': jobDescription,
            }


