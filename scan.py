#!/usr/bin/python3

# global imports
import requests
import re
import urllib.parse
from bs4 import BeautifulSoup
from termcolor import colored

#local imports
import payloads

class Scanner:
    def __init__(self, url, payload_type, payload_codes):
        self.session = requests.Session()
        self.target_url = url
        self.target_links = [url]
        self.payloads = []
        sample_payload = payloads.types[payload_type]
        for i in payload_codes:
            self.payloads.append(payloads.get_payload(sample_payload, i))


        

    # function to get full url with parameters
    def get_full_url(self, url):
        response = requests.get(url)
        full_url = response.url
        return full_url

    # function to extract links(<a> tags) from a webpage
    def extract_links_from(self, url):
        response = self.session.get(url)
        return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))

    # function to crawl a site
    def crawl(self, url=None):
        if url == None:
            url = self.target_url   
        href_links = self.extract_links_from(url)
        for link in href_links:
            link = urllib.parse.urljoin(url, link)

            if "#" in link:
                link = link.split("#")[0]
            if self.target_url in link and link not in self.target_links:
                link = self.get_full_url(link)
                self.target_links.append(link)
                self.crawl(link)

    # function to extract form tags from a webpage
    def extract_forms(self, url):
        response = self.session.get(url)
        parsed_html = BeautifulSoup(str(response.content), "html.parser")
        forms_list = parsed_html.findAll("form")
        return forms_list
    
    def submit_form(self, form, value, url):
        action = form.get("action")
        post_url = urllib.parse.urljoin(url, action)

        method = form.get("method")    

        inputs_list = form.findAll("input")
        post_data = {}
        for i in inputs_list:
            input_name = i.get("name")
            input_type = i.get("type")
            input_value = i.get("value")
            if input_type == "text":
                input_value = value
            post_data[input_name] = input_value
        if method == "post":
            return self.session.post(post_url, data=post_data)
        return self.session.get(post_url, params=post_data)
    
    def run_scanner(self):
        is_vuln = False
        for link in self.target_links:
            forms = self.extract_forms(link)
            for form in forms:
                is_vulnerable_to_xss = self.test_xss_in_form(form, link)
                if is_vulnerable_to_xss[0]:
                    print(colored("XSS vulnerability in FORM", "green") +
                          f" — {link}")
                    print(f"|   Payload used: {is_vulnerable_to_xss[1]}")
                    is_vuln = True
            if "=" in link:
                is_vulnerable_to_xss = self.test_xss_in_link(link)
                if is_vulnerable_to_xss[0]:
                    print(colored("XSS vulnerability in FORM", "green") +
                          f" — {link}")
                    print(f"|   Payload used: {is_vulnerable_to_xss[1]}")
                    is_vuln = True
        if not is_vuln:
            print(colored("Vulnerabilities were not found", "red"))

    # Checking if link is vulnerable for XSS attack 
    def test_xss_in_link(self, url):
        for payload in self.payloads:
            url = url.replace("=", f"={payload}")
            response = self.session.get(url)
            if payload.encode() in response.content:
                return [True, payload]
        return [False, None]

    # Checking if FORM is vulnerable for XSS attack
    def test_xss_in_form(self, form, url):
        for payload in self.payloads:
            response = self.submit_form(form, payload, url)
            if payload.encode() in response.content:
                return [True, payload]
        return [False, None]

