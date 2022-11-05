import scrapy




class CandidateInformation(scrapy.Spider):
    name = 'CandidateInfo'
    allowed_domains = ['ballotpedia.org']
    def __init__(self, candidate_url):
        print("into CandidateInformation class")
        print('candidate url = ',candidate_url)
        self.candidate_url = candidate_url
        # self.start_requests()

    def start_requests(self):
        print("into start_requests")
        # yield scrapy.Request(url=self.candidate_url, callback=self.parse) 
        scrapy.Request(url=self.candidate_url, callback=self.parse) 

    def parse(self, response):
        print('into parse')
        # info_box = driver_candidate_info.find_element(By.XPATH, "//div[@class='infobox person']")
        info_box = response.xpath("//div[@class='infobox person']").get()
        print("*"*70)
        # name = info_box.find_element(By.XPATH, "./div[1]").text
        name = info_box.xpath("./div[1]/text()").get()
        print("Name = ",name)
        # photo_url = info_box.find_element(By.XPATH, "./div[2]//img").get_attribute('src')
        photo_url = info_box.xpath("./div[2]//img/attr(src)").get()
        print('photo url = ', photo_url)
        # party = info_box.find_element(By.XPATH, "./div[3]").text
        party = info_box.xpath("./div[3]/text()").get()
        print("Party = ",party)


class StateUrls(scrapy.Spider):
    name = 'StateUrls'
    allowed_domains = ['ballotpedia.org']
    # def __init__(self, state_url):
    #     print("into StateUrls class")
    #     print('state_url url = ',state_url)
    #     self.state_url = state_url
    #     # self.start_requests()
    start_urls = ['https://ballotpedia.org/Elections_by_state_and_year']
    # def start_requests(self):
    #     print("into start_requests")
    #     # yield scrapy.Request(url=self.candidate_url, callback=self.parse) 
    #     yield scrapy.Request(url=self.state_url, callback=self.parse) 

    def parse(self, response):
        print('into parse')
        body_content = response.xpath("//div[@class='mw-parser-output']")
        all_h2 = body_content.xpath("//h2/text()").getall()
        for h2 in all_h2:
            print(h2)
        print("*"*70)
       