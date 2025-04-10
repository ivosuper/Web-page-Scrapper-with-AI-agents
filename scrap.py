import requests
from bs4 import BeautifulSoup

url = "https://www.sportdepot.bg/product/adidas_performance_obuvki_galaxy_7_running_graphic-N_JH7861-basic.html?rlv_rid=c167ac7f-d4f0-47ef-a554-426e67114017&rlv_rpid=bg_JH7861&rlv_rpos=3"
# url = "https://www.sportdepot.bg/product/nike_obuvki_revolution_7-N_FB2207-001-basic.html?i=28329&complects="

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")
title = doc.find('h1', class_='page-title product-title').find('span', {'data-product-number': 'name-formated'}).string
price = doc.find('div', {'data-product-number': 'prices'}).find('span', class_='current').string

variants_colors = doc.find('div', class_='product-color-section').find('div', class_='product-colors').find_all(attrs={'data-color': 'value'})
# for colors in variants_colors:
#     print(colors.text)
variants_sizes = doc.find('div', class_='product-size-section').find('ul').find_all('li')

availability = doc.find('button', class_='btn-availability').string
meta_title = doc.find('div', class_='product-short-description').string
meta_description = doc.find('div', {'data-product-number': 'description'}).text

print(title)
print(price)
print(variants_colors)
print(variants_sizes)
print(availability)
print(meta_title)
print(meta_description)

# print(doc.prettify())

