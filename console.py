import requests, re, os, json
from bs4 import BeautifulSoup
from requests.api import get

url = 'https://www.usatoday.com'
req = requests.get(url)
bs = BeautifulSoup(req.text, 'lxml')
lst = bs.select(".gnt_m_th_a")

def get_news():
  for li in lst:
    href = url + li["href"]
    r = requests.get(href)
    b = BeautifulSoup(r.text, 'lxml')
    texts = b.select("div.gnt_ar_b > p.gnt_ar_b_p")

    contents = list(p.text for p in texts)
    contents =  ' '.join(contents)
    return contents.lower()
  
  return None

def translate(words):
  try:
    url = 'https://ac-dict.naver.com/enko/ac?st=11&r_lt=11&q={}'.format(words)
    r = requests.get(url)
    j = json.loads(r.text)
    return (j["items"][0][0][2][0])
  except:
    return None

def make_dict(news):
  match_pat = re.findall(r'\b[a-z]{4,15}\b',news)
  frequency = dict()
  ret = list()
  for word in match_pat:
    count = frequency.get(word, 0)
    frequency[word] = count + 1
  
  for word, cnt in frequency.items():
    if (cnt > 1):
      kr = translate(word)
      if (kr != None):
        ret.append({kr : word})
  return ret

print(make_dict(get_news()))
