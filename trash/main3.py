# import pandas as pd
from httpx import Client
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from pydantic_ai.exceptions import UnexpectedModelBehavior
from models import OLLAMA_MODEL, ANTHROPIC_MODEL, GEMINI_MODEL



# agent = Agent(
#     model=OLLAMA_MODEL,
#     system_prompt=['You are a helpful AI assistant']
# )

# response = agent.run_sync('Hi how are you ?')
# print(response.data)

class Product(BaseModel):
    title: str = Field(title='Product Name', description="The title of the product.")
    price: float = Field(title='Price', description="The price of the product.")
    variants: list = Field(title='Variants', description="A list of product variants (e.g., size, color).")
    availability: str = Field(title='Availability', description="The availability status of the product (e.g., 'In stock', 'Out of stock').")
    meta_title: str = Field(title='Short Description', description="The meta title (short description) of the product page.")
    meta_description: str = Field(title='Long Description', description="The meta description (long description) of the product page.")

class Results(BaseModel):
    dataset: list[Product] = Field(title='Dataset', description='The list of products')

web_scraping_agent = Agent(
    name='Web Scraping Agent',
    model=OLLAMA_MODEL,
    system_prompt="""
    Your task is to convert a data string into a list of dictionaries.

    Step 1. Fetch the HTML text from the given URL using the fetch_html_text() function.
    Step 2. Takes the output from Step 1 and clean up for the final output.
    """,
        retries=2,
        result_type=Results,
        model_settings=ModelSettings(
            max_tokens=8000,
            temperature=0.1
        ),
    )

@web_scraping_agent.tool_plain(retries=1)
def fetch_html_text(url: str) -> str:
    """
    Fetches the HTML text from a given URL

    args:
        url: str - The page's URL to fetch the HTML text from

    returns:
        str: The HTML text from the given URL
    """
    print(f"Calling URL: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    with Client(headers=headers) as client:
        response = client.get(url, timeout=20)
    if response.status_code != 200:
        return f"Failed to fetch the HTML text from {url}. Status code: {response.status_code}"
    soup = BeautifulSoup(response.text, 'html.parser')
    with open('soup.txt', 'w', encoding='utf-8') as f:
        f.write(soup.get_text())
    print('Soup file saved')
    return soup.get_text().replace('\n', '').replace('\r', '')

def main() -> None:
    url = "https://www.sportdepot.bg/product/adidas_performance_obuvki_galaxy_7_running_graphic-N_JH7861-basic.html?rlv_rid=c167ac7f-d4f0-47ef-a554-426e67114017&rlv_rpid=bg_JH7861&rlv_rpos=3"
    url = "https://www.sportdepot.bg/product/nike_obuvki_revolution_7-N_FB2207-001-basic.html?i=28329&complects="
    # url = "https://www.sportdepot.bg/muje-obuvki/sportni_obuvki-2_77_51"
    prompt = url
    try:
        response = web_scraping_agent.run_sync(prompt)
        if response.data is None:
            return None
        print("." * 50)
        print("Input tokens:", response.usage().request_tokens)
        print("Output tokens:", response.usage().response_tokens)
        print("Total tokens:", response.usage().total_tokens)
        print(response.data.dataset)
        print(response)


        # lst = []
        # for item in response.data.dataset:
        #     lst.append(item.model_dump())
        # print(lst)
        # timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # df = pd.DataFrame(lst)
        # df.to_csv(f"product_listings_{timestamp}.csv", index=False)
    except UnexpectedModelBehavior as e:
        print(e)
main()