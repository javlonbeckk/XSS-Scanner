#!/usr/bin/python3

#global imports
import requests
from bs4 import BeautifulSoup
import requests
from Wappalyzer import Wappalyzer, WebPage

# Checking if a website is working
def is_alive(url):
    response = requests.head(url)
    status_code = response.status_code

    if status_code == 200:
        return True
    else:
        return False

# Identifying protocol(http or https)
def check(site):
    try:     
        res = requests.get(f"http://{site}")
        if res.status_code == 200:
            return "http"
    except Exception:
        pass

    try:
        res = requests.get(f"https://{site}")
        if res.status_code == 200:
            return "https"
    except Exception:
        pass

    return ""

# function to get info about technologies used in a website
def get_technologies(target):
    res = ""
    page = requests.get(target)
    soup = BeautifulSoup(page.content, 'html.parser')
    if soup.title:
        title = soup.title.text
    else:
        title = ""

    title = f"TITLE: {title}"

    try:
        wappalyzer = Wappalyzer.latest()
        webpage = WebPage.new_from_url(target)
        technologies = wappalyzer.analyze_with_versions_and_categories(webpage)

        res += "TECHNOLOGIES:\n"

        di = {}
        for tech in technologies:
            category = technologies[tech]['categories'][0]
            if technologies[tech]['versions']:
                version = technologies[tech]['versions'][0]
            else:
                version = ""

            if category in di.keys():
                di[category] += [{tech:version}]
            else:
                di[category] = [{tech:version}]
            
        for category in di:
            res += f"|  {category}:\n"
            for i in di[category]:
                for j in i.keys():
                    res += f"|      {j} {i[j]}\n"
        if "\n" in res:
            res = res[:-2]
        return [title, res]
    except Exception:
        return ["", ""]
    
    
def get_time(duration):
    duration = str(duration)
    duration = duration.split(":")

    hours = int(duration[0])
    minutes = int(duration[1])
    seconds = int(duration[2].split(".")[0])
    miniseconds = duration[2].split(".")[1][:2]

    res = str(hours*3600 + minutes*60 + seconds) + "."+ miniseconds
    return res