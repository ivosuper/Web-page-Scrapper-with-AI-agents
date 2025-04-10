import requests
from bs4 import BeautifulSoup, Comment
import re

url = "https://www.sportdepot.bg/product/adidas_performance_obuvki_galaxy_7_running_graphic-N_JH7861-basic.html?rlv_rid=c167ac7f-d4f0-47ef-a554-426e67114017&rlv_rpid=bg_JH7861&rlv_rpos=3"
# url = "https://www.sportdepot.bg/product/nike_obuvki_revolution_7-N_FB2207-001-basic.html?i=28329&complects="

result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")

for tag in soup.find_all(['script', 'style', 'link', 'meta', 'head', 'nav', 'footer', 'aside', 'img']):
        tag.decompose()

for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
    comment.extract()

print(str(soup).replace('\n\n', '').replace('\r\r', ''))
print(type(soup))

