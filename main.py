import requests
import html2text
import csv
import pandas as pd

# URL to Text via Readability API
API_TOKEN = *API TOKEN*
base_url = 'https://readability.com'
target_url = ''

def url_builder(target_url):
    return '%s/api/content/v1/parser?url=%s&token=%s' % (base_url, target_url, API_TOKEN)

    #Retrevies JSON
def get_json(target_url):
    resp = requests.get(url_builder(target_url))
    return resp

def get_content(target_url):
    resp = requests.get(url_builder(target_url))
    if 'content' in resp.json():
        html_content = resp.json()['content']
        content=html2text.html2text(html_content)
        return content
    else:
        content='Error retreving text'
    return content

df=pd.read_csv('links.csv', names={'links'})

text_list=[]
for link in df['links'][100:125]:
    url=link
    text=get_content(link).encode("ascii", "ignore")
    brand=sum(text.count(x) for x in ("Steelcase", "steelcase"))
    newswire=text.count("PRNewswire")

    text_list.append({'Url':url, 'Text':text, 'Steelcase':brand, 'Newswire':newswire})
    
pd.DataFrame(text_list).to_excel('export.xlsx', index=False)