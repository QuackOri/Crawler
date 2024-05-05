import requests
from bs4 import BeautifulSoup
import re

current_urls = {}
later_urls = {}
visited_urls = {}

def visit_onion(onion_url, referer):
    global later_urls

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
            url_text = a_tag.get('href')
            if url_text is not None and url_text.startswith('http'):
                child_domain.append(url_text)
        row = {
            "name": "TEST",
            "origin_url": onion_url,
            "parameter": parameter,
            "title": title,
            "url": url_buffer,
            "domain": domain,
            "HTML": response.text,
            "wordlist": words,
            "referer": referer
        }
        response = requests.post("http://uskawjdu.iptime.org:8001/postData", json=row)
        print(response.status_code)
        
        later_urls[onion_url] = child_domain
    else:
        print(onion_url, response.status_code, response.headers)
    return True
    

def repeat(depth):
    global current_urls
    global later_urls
    global visited_urls

    for _ in range(depth):
        current_urls = later_urls
        later_urls = {}
        for referer, urls in current_urls.items():
            for url in urls:
                if url in visited_urls:
                    continue
                else:
                    visited_urls[url] = True
                    print("Crawling", url)
                    visit_onion(url, referer)
        


# test_url = 'http://1guy2biketrips.michaelahgu3sqef5yz3u242nok2uczduq5oxqfkwq646tvjhdnl35id.onion/'
response = requests.get("http://uskawjdu.iptime.org:8001/getUrl?name=TEST")
data = response.json()
later_urls[""] = [data['url']]
repeat(data['Depth'])
