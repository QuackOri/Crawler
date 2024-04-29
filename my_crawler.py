import requests
from bs4 import BeautifulSoup
import sys, re

def visit_onion(onion_url):
    proxies = {
        "http" : "socks5h://127.0.0.1:9050",
        "https" : "socks5h://127.0.0.1:9050"
    }
    try:
        response = requests.get(onion_url, proxies=proxies, allow_redirects=True)
        response.close()
    except Exception as e:
        print(onion_url, e)
        return False
    if response.status_code == 200:
        if "https" in onion_url:
            protocol_index = 8
        else:
            protocol_index = 7

        param_index = onion_url.find("?")
        if param_index > 0:
            parameter = onion_url[param_index:]
            url_buffer = onion_url[:param_index]
        else:
            parameter = ""
            url_buffer = onion_url

        domain_index = url_buffer[protocol_index:].find("/")
        if domain_index > 0:
            domain = url_buffer[protocol_index:domain_index]
        else:
            domain = url_buffer[protocol_index:]
        
        # with open(url_buffer[protocol_index:] + ".html", "wb") as f:
        #     f.write(response.content)

        soup = BeautifulSoup(response.content, "html.parser")
        title = str(soup.title)
        title = title.replace("<title>","").replace("</title>", "")

        text_without_punctuation = re.sub(r'[^\w ]', '', soup.text)
        words = text_without_punctuation.split()

        child_domain = []
        for a_tag in soup.find_all('a'):
            child_domain.append(a_tag.get('href'))

        row = {
            'origin_url': onion_url,
            'parameter': parameter,
            'title': title,
            'url': url_buffer,
            'domain': domain,
            "HTML": response.content,
            "wordlist": words,
            "isCrawling": True
        }
        response = requests.post("http://uskawjdu.iptime.org:8001/postData", data=row)
        print(response.status_code)
        # print(child_domain)
    else:
        print(onion_url, response.status_code, response.headers)
    return True
    
tmp_list = []
onion_url = sys.argv[1]
visit_onion(onion_url)