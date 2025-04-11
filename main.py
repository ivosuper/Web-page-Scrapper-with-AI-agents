import sys
import requests
from bs4 import BeautifulSoup, Comment
from pydantic import BaseModel, Field
from pydantic_ai import Agent, Tool
from pydantic_ai.settings import ModelSettings
from models import OLLAMA_MODEL, ANTHROPIC_MODEL, GEMINI_MODEL

if sys.argv[1] :
    url = sys.argv[1]
else:
    url = input("Paste URL (q for exit): ")

if url.lower() == 'q':
            print("Bye")
            sys.exit()

# Uncomment some of this lines if you do not want to paste it like argument
# url = "https://www.sportdepot.bg/product/adidas_performance_obuvki_galaxy_7_running_graphic-N_JH7861-basic.html?rlv_rid=c167ac7f-d4f0-47ef-a554-426e67114017&rlv_rpid=bg_JH7861&rlv_rpos=3"
# url = "https://www.sportdepot.bg/product/nike_obuvki_revolution_7-N_FB2207-001-basic.html?i=28329&complects="

try:
    request_result = requests.get(url)
    request_result.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    request_result.text
except requests.exceptions.HTTPError as e:
    print(f"Page not found or error occurred: {e}")
    sys.exit()
except requests.exceptions.RequestException as e:  # Catch other request errors (e.g., connection errors)
    print(f"An error occurred while making the request: {e}")
    sys.exit()

soup = BeautifulSoup(request_result.text, "html.parser")

# Clean the HTML to be less context, tokens and more understandable for the AI model. Can be done even better.
for tag in soup.find_all(['script', 'style', 'link', 'meta', 'head', 'nav', 'footer', 'aside', 'img']):
        tag.decompose()

for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
    comment.extract()

cleaned_html = str(soup).replace('\n\n', '').replace('\r\r', '')

#TODO The scraping agent can be with improved prompts and to have validators and tools for data processing. Without second agent. 

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

print("Title: ", response.data.title)
print("Price: ", response.data.price)
print("Variants: ", response.data.variants)
print("Availability: ", response.data.availability)
print("Short description: ", response.data.meta_title)
print("Meta description: ", response.data.meta_description)

#TODO the second agent use  tool and dependency for example.
class ValidResultResponse(BaseModel):
    valid_price: bool = Field(title='Valid Price', description="Is the price a valid number")
    valid_availibility: bool = Field(title='Valid Availability', description="Confirm that availability includes the word 'In stock' or 'Out of stock'")
    valid_valriants_of_the_product: bool = Field(title='Valid Variants', description="Ensure variant names and options are non-empty if provided")


ProductValidatorAgent = Agent(
    model=GEMINI_MODEL,
    result_type=ValidResultResponse,
    system_prompt=[
         'Your only taks is validating extracted product information.'
         'Use the tool to respond to the cliend the data is valid.'
         ],
    retries=1,
    model_settings=ModelSettings(
        max_tokens=8000,
        temperature=0.1
    ),
)
# Very simple tool just to have one for example how the Agent call it.
@ProductValidatorAgent.tool_plain
def respond_to_user():
     print("." * 50)
     print('The data is valid. Response form the TOOL')
     print("." * 50)



#TODO here we can use dependencies for structured input and tools to change the data types for the the price  and the currency BGN EU USD and more. 
#TODO agents can be connected diferent way ot this agent to be called from tool of the first agent. have many options.
simple_prompt = f"Price: {response.data.price} Availability: {response.data.availability} Variants: {response.data.variants}"

validation_response = ProductValidatorAgent.run_sync(simple_prompt)
print("." * 50)
print("Input tokens:", validation_response.usage().request_tokens)
print("Output tokens:", validation_response.usage().response_tokens)
print("Total tokens:", validation_response.usage().total_tokens)
print("." * 50)
data = validation_response.data
print("Is the price valid: ", data.valid_price)
print("Is the availability valid: ", data.valid_availibility)
print("Is the variants valid: ", data.valid_valriants_of_the_product)
print("." * 50)

