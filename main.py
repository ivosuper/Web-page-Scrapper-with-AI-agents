import requests
from bs4 import BeautifulSoup, Comment
from pydantic import BaseModel, Field
from pydantic_ai import Agent, Tool
from pydantic_ai.settings import ModelSettings
from models import OLLAMA_MODEL, ANTHROPIC_MODEL, GEMINI_MODEL

# url = "https://www.sportdepot.bg/product/adidas_performance_obuvki_galaxy_7_running_graphic-N_JH7861-basic.html?rlv_rid=c167ac7f-d4f0-47ef-a554-426e67114017&rlv_rpid=bg_JH7861&rlv_rpos=3"
url = "https://www.sportdepot.bg/product/nike_obuvki_revolution_7-N_FB2207-001-basic.html?i=28329&complects="

request_result = requests.get(url)
soup = BeautifulSoup(request_result.text, "html.parser")

for tag in soup.find_all(['script', 'style', 'link', 'meta', 'head', 'nav', 'footer', 'aside', 'img']):
        tag.decompose()

for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
    comment.extract()

cleaned_html = str(soup).replace('\n\n', '').replace('\r\r', '')

class Product(BaseModel):
    title: str = Field(title='Product Name', description="The title of the product.")
    price: str = Field(title='Price', description="The price of the product.")
    variants: str = Field(title='Variants', description="A list of product variants (e.g., size, color).")
    availability: str = Field(title='Availability', description="The availability status of the product (e.g., 'In stock', 'Out of stock').")
    meta_title: str = Field(title='Short Description', description="The meta title (short description) of the product page.")
    meta_description: str = Field(title='Long Description', description="The meta description (long description) of the product page. Hint: The long descriptin is in tab 'Информация за продукта'")

ProductInfoAgent = Agent(
    model=GEMINI_MODEL,
    result_type=Product,
    system_prompt=[
        'Fetch the description of a product Like the product name, price variants like colors, sizes, avalibility it is in stock or not. The short description and the long description of the product, from scraped html cleaned from all tags'
        'The represented imput is verry messy you need to find in this html or text mess the velues that you search for.'
        # 'Hints: Price is in div class data-product-number, span class current '
        ],
    retries=1,
    model_settings=ModelSettings(
        max_tokens=8000,
        temperature=0.1
    ),
)

response = ProductInfoAgent.run_sync(cleaned_html)

print("." * 50)
print("Input tokens:", response.usage().request_tokens)
print("Output tokens:", response.usage().response_tokens)
print("Total tokens:", response.usage().total_tokens)
print("." * 50)
print(response.data)

class ValidResultResponse(BaseModel):
    valid_price: bool = Field(title='Valid Price', description="Is the price a valid number")
    valid_availibility: bool = Field(title='Valid Price', description="Confirm that availability includes the word 'In stock' or 'Out of stock'")
    valid_valriants_of_the_product: bool = Field(title='Valid Price', description="Ensure variant names and options are non-empty if provided")

ProductValidatorAgent = Agent(
    model=GEMINI_MODEL,
    result_type=ValidResultResponse,
    system_prompt=['Your only taks is validating extracted product information.'],
    retries=10,
    model_settings=ModelSettings(
        max_tokens=8000,
        temperature=0.1
    ),
)

print(type(response.data))
# response = ProductValidatorAgent.run_sync(response.data)
# print("." * 50)
# print("Input tokens:", response.usage().request_tokens)
# print("Output tokens:", response.usage().response_tokens)
# print("Total tokens:", response.usage().total_tokens)
# print("." * 50)
# print(response.data)

