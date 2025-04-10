import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from pydantic_ai import Agent, Tool
from models import OLLAMA_MODEL, ANTHROPIC_MODEL, GEMINI_MODEL

# Define Pydantic models for data extraction
class ProductInfo(BaseModel):
    title: str = Field(..., description="The title of the product.")
    price: float = Field(..., description="The price of the product.")
    variants: list = Field(None, description="A list of product variants (e.g., size, color).")
    availability: str = Field(..., description="The availability status of the product (e.g., 'In stock', 'Out of stock').")
    meta_title: str = Field(..., description="The meta title of the product page.")
    meta_description: str = Field(..., description="The meta description of the product page.")

# Define tools for the agents
def extract_product_info(html_content: str) -> ProductInfo:
    """Extracts product information from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Example extraction (adjust selectors based on the website structure)
    title = soup.find('h1').text.strip() if soup.find('h1') else "Title not found"
    try:
        price_str = soup.find('span', class_='price').text.strip().replace(',', '.')
        price = float(price_str)
    except:
        price = 0.0
    availability = "In stock" if soup.find('div', class_='availability') else "Out of stock"
    meta_title = soup.find('meta', attrs={'name': 'title'})['content'] if soup.find('meta', attrs={'name': 'title'}) else "Meta title not found"
    meta_description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else "Meta description not found"

    return ProductInfo(
        title=title,
        price=price,
        variants=[],
        availability=availability,
        meta_title=meta_title,
        meta_description=meta_description
    )

def validate_product_info(product_info: ProductInfo) -> str:
    """Validates the extracted product information."""
    if not isinstance(product_info.price, (int, float)):
        return "Invalid price format."
    if not isinstance(product_info.price, float):
        try:
            float(product_info.price)
        except:
            return "Price is not a number"
    if not ("In stock" in product_info.availability or "Out of stock" in product_info.availability):
        return "Invalid availability status."
    if product_info.variants and not all(product_info.variants):
        return "Variant names or options are empty."
    return "Product information is valid."

# Define the agents
class ProductInfoAgent(Agent):
    def __init__(self):
        super().__init__(
            description="Extracts product information from a product page URL.",
            tools=[Tool(name="extract_product_info", function=extract_product_info)]
        )

    async def run(self, url: str) -> ProductInfo:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        return await self.tool("extract_product_info", html_content=html_content)

class ProductValidatorAgent(Agent):
    def __init__(self):
        super().__init__(
            description="Validates the extracted product information.",
            tools=[Tool(name="validate_product_info", function=validate_product_info)]
        )

    async def run(self, product_info: ProductInfo) -> str:
        return await self.tool("validate_product_info", product_info=product_info)
    
# Example usage
async def main():
    product_url = "https://www.sportdepot.bg/product/adidas_performance_obuvki_galaxy_7_running_graphic-N_JH7861-basic.html?rlv_rid=c167ac7f-d4f0-47ef-a554-426e67114017&rlv_rpid=bg_JH7861&rlv_rpos=3"

    product_info_agent = ProductInfoAgent()
    product_info = await product_info_agent.run(product_url)

    print("Extracted Product Info:", product_info)

    validator_agent = ProductValidatorAgent()
    validation_result = await validator_agent.run(product_info)

    print("Validation Result:", validation_result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())