from functools import lru_cache
import os
from pathlib import Path
import getpass

def get_api_key_from_user():
    """Get OpenAI API key from user input."""
    print("🔑 OpenAI API Key Required")
    print("=" * 40)
    print("You need an OpenAI API key to use translate-pptx.")
    print("Get your API key from: https://platform.openai.com/api-keys")
    print()
    
    # Try to get API key from environment variable first
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and api_key != 'your_openai_api_key_here':
        print("✅ Using API key from environment variable")
        return api_key
    
    # If not available, prompt user to input
    while True:
        api_key = getpass.getpass("Enter your OpenAI API key: ").strip()
        if api_key:
            # Set environment variable for this session
            os.environ['OPENAI_API_KEY'] = api_key
            print("✅ API key set successfully")
            return api_key
        else:
            print("❌ No API key provided. Please try again.")

@lru_cache(maxsize=128)
def prompt_openai(message: str, model="gpt-4o-2024-11-20", api_key=None):
    """A prompt helper function that sends a message to openAI
    and returns only the text response.
    Results are cached to optimize for repeated queries.
    """
    import openai
    
    # Get API key from parameter, environment, or user input
    if api_key is None:
        api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key or api_key == 'your_openai_api_key_here':
        api_key = get_api_key_from_user()
    
    if not api_key:
        raise ValueError("OpenAI API key is required to use this function.")

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
