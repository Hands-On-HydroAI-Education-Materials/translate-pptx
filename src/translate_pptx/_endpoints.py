from functools import lru_cache
import os
from pathlib import Path
import getpass
import sys

def _is_notebook_environment():
    """Check if running in a Jupyter notebook environment."""
    try:
        # Check for IPython/Jupyter environment
        from IPython import get_ipython
        if get_ipython() is not None:
            # Check if in notebook (not IPython shell)
            if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
                return True
    except ImportError:
        pass
    return False

def _get_api_key_input():
    """Get API key input with notebook compatibility."""
    if _is_notebook_environment():
        try:
            # Try to use getpass first (works in newer notebooks)
            import getpass
            return getpass.getpass("Enter your OpenAI API key: ").strip()
        except (OSError, AttributeError):
            # Getpass doesn't work in some notebook environments
            try:
                # Try to use ipywidgets for secure input
                from ipywidgets import widgets
                from IPython.display import display, clear_output
                import asyncio
                
                # Create password widget
                password_widget = widgets.Password(
                    placeholder='sk-...',
                    description='API Key:',
                    disabled=False,
                    style={'description_width': 'initial'},
                    layout=widgets.Layout(width='400px')
                )
                
                # Create submit button
                submit_button = widgets.Button(
                    description="Submit", 
                    button_style='primary',
                    layout=widgets.Layout(width='100px')
                )
                
                # Create output widget for messages
                output = widgets.Output()
                
                # Container for the widgets
                container = widgets.VBox([
                    widgets.HTML("<b>Enter your OpenAI API key:</b>"),
                    password_widget, 
                    submit_button,
                    output
                ])
                
                # Variable to store the result
                result = {'api_key': None, 'submitted': False}
                
                def on_submit(b):
                    with output:
                        clear_output(wait=True)
                        if password_widget.value:
                            result['api_key'] = password_widget.value
                            result['submitted'] = True
                            print("✅ API key submitted successfully")
                        else:
                            print("❌ Please enter your API key")
                
                submit_button.on_click(on_submit)
                
                # Handle Enter key press
                def handle_submit(change):
                    if change['type'] == 'change' and change['name'] == 'value':
                        # Auto-submit when user presses Enter
                        pass
                
                password_widget.observe(handle_submit)
                
                display(container)
                
                # Wait for user input
                import time
                while not result['submitted']:
                    time.sleep(0.1)
                
                # Clear the widget after submission
                clear_output(wait=True)
                return result['api_key']
                
            except ImportError:
                # Fallback to regular input if ipywidgets not available
                print("💡 Tip: For secure password input in notebooks, install ipywidgets:")
                print("   pip install ipywidgets")
                print("   jupyter nbextension enable --py widgetsnbextension")
                print()
                return input("Enter your OpenAI API key: ").strip()
    else:
        # Use getpass for terminal environments
        return getpass.getpass("Enter your OpenAI API key: ").strip()

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
        try:
            api_key = _get_api_key_input()
            if api_key:
                # Set environment variable for this session
                os.environ['OPENAI_API_KEY'] = api_key
                print("✅ API key set successfully")
                return api_key
            else:
                print("❌ No API key provided. Please try again.")
        except KeyboardInterrupt:
            print("\n❌ Cancelled by user")
            return None
        except Exception as e:
            print(f"❌ Error getting input: {e}")
            print("Falling back to regular input...")
            api_key = input("Enter your OpenAI API key: ").strip()
            if api_key:
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

def set_openai_api_key(api_key=None):
    """
    Set OpenAI API key for the current session.
    
    This function is especially useful in Jupyter notebooks where you can
    call it once at the beginning of your session.
    
    Args:
        api_key (str, optional): Your OpenAI API key. If not provided,
                               you'll be prompted to enter it.
    
    Example:
        # In a Jupyter notebook cell:
        from translate_pptx import set_openai_api_key
        set_openai_api_key()  # Will prompt for key
        
        # Or directly:
        set_openai_api_key("sk-your-key-here")
    """
    if api_key is None:
        api_key = get_api_key_from_user()
    
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
        print("✅ OpenAI API key has been set for this session")
        return True
    else:
        print("❌ Failed to set API key")
        return False

def prompt_nop(message:str):
    """A prompt helper function that does nothing but returns the contained json. This function is useful for testing."""
    return "```json" + message.split("```json")[1]
