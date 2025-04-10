from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.gemini import GeminiModel
from dotenv import load_dotenv

# Load environment variables from .env file. Set the API key for Cloud Sonet Anthropic
load_dotenv()

model = 'gemma3:12b'
model = 'llama3.2:latest'
# model = 'llama3.1:latest'

OLLAMA_MODEL = OpenAIModel(
    model_name = model,
    provider = OpenAIProvider(base_url = 'http://localhost:11434/v1')
)

ANTHROPIC_MODEL = AnthropicModel('claude-3-5-sonnet-latest')
GEMINI_MODEL = GeminiModel('gemini-2.0-flash', provider='google-gla')