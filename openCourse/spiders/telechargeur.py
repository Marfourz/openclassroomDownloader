import scrapy
import requests
import os
import re

class Telechargeur(scrapy.Spider):
    name = 'Telechargeur'
    def start_requests(self):
        urls = ["https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python.html"]
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)
    
    def parse(self,response):
        yield scrapy.Request(url = response.url, callback = self.creatorDir)
        for url in response.css("li.course-part-summary__item h4 a::attr(href)").getall():
            url = response.urljoin(url)
            yield scrapy.Request(url = url, callback = self.creatorDir)
    

    def creatorDir(self,response):
        print("salut me voici " + response.url)
        page = response.url.split("/")[-1] + "-inter" + ".html"
        filename = page
        with open(filename, 'wb') as f:
            f.write(response.body)
        os.mkdir((response.url.split('/')[-1]))
        liens = response.css("link::attr(href)").getall() + response.css("img::attr(src)").getall() + response.css("script::attr(src)").getall()
        for lien in liens:
            if lien.startswith("/"):
                lien = lien[1:]
            print(lien + "\n")
            baseDirectory = response.url.split('/')[-1]
            lienList = lien.split("/")[:-1]
            for dirname in lienList :
                if not os.path.isdir(os.path.join(baseDirectory,dirname)):
                    os.mkdir(os.path.join(baseDirectory,dirname))
                baseDirectory = os.path.join(baseDirectory,dirname)
            media = requests.get("https://openclassrooms.com/"+lien).content
            with open(response.url.split('/')[-1] + "/" + lien,"wb") as f :
                f.write(media)

        f1 = open(filename,'rb')
        f2 = open(response.url.split("/")[-1] + ".html" ,'w')
        patternLien = "a.*href=\""
        pattern = "(src=\")|(href=\")"
        for line in f1:
            line = line.decode()
            matchLien = re.search(patternLien, line)
            match = re.search(pattern,line)
            if matchLien :
                fin = line.find("\"",matchLien.end())
                line = list(line)
                line[matchLien.end():fin] = list((''.join(line[matchLien.end():fin])).split("/")[-1]+".html")
                line = (''.join(line))
            elif match :
                line = list(line)
                line.insert(match.end(),response.url.split("/")[-1])
                line = ''.join(line)
            f2.write(line)
        f1.close()
        f2.close()
        os.remove(filename)

            
            


        
        




    
