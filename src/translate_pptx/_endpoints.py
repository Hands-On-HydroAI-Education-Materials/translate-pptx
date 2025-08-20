from functools import lru_cache
import os
from pathlib import Path

def load_dotenv():
    """Load environment variables from .env file if it exists."""
    try:
        from dotenv import load_dotenv as _load_dotenv
        # Look for .env file in current directory and parent directories
        current_dir = Path.cwd()
        for parent in [current_dir] + list(current_dir.parents):
            env_file = parent / '.env'
            if env_file.exists():
                _load_dotenv(env_file)
                break
    except ImportError:
        # python-dotenv not installed, continue without it
        pass

@lru_cache(maxsize=128)
def prompt_openai(message: str, model="gpt-4o-2024-11-20"):
    """A prompt helper function that sends a message to openAI
    and returns only the text response.
    Results are cached to optimize for repeated queries.
    """
    import openai
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if API key is available
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError(
            "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable "
            "or create a .env file with your API key. You can copy .env.example to .env "
            "and fill in your actual API key."
        )

    message = [{"role": "user", "content": message}]

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=message
    )
    return response.choices[0].message.content

def prompt_nop(message:str):
    """A prompt helper function that does nothing but returns the contained json. This function is useful for testing."""
    return "```json" + message.split("```json")[1]
