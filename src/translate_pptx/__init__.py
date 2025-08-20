__version__ = "0.1.1"

# Import main functions for easy access
from ._endpoints import set_openai_api_key, prompt_openai
from ._pptx import extract_text_from_slides, replace_text_in_slides
from ._translation import translate_data_structure_of_texts_recursive

# Make commonly used functions available at package level
__all__ = [
    'set_openai_api_key',
    'prompt_openai', 
    'extract_text_from_slides',
    'replace_text_in_slides',
    'translate_data_structure_of_texts_recursive'
]
