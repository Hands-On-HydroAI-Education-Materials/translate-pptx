# translate-pptx
[![PyPI](https://img.shields.io/pypi/v/translate-pptx.svg?color=green)](https://pypi.org/project/translate-pptx)
[![License](https://img.shields.io/pypi/l/translate-pptx.svg?color=green)](https://github.com/haesleinhuepf/translate-pptx/raw/main/LICENSE)

translate-pptx is a command line tool that translates PowerPoint PPTX files from one language to another.

![banner](https://github.com/haesleinhuepf/translate-pptx/raw/main/docs/images/banner.png)

## Usage

### Basic Usage

The simplest way to translate a PowerPoint presentation:

```bash
translate-pptx my_slides.pptx german
```

This will create a new file named `my_slides_german.pptx` with the translated content.

### Advanced Usage

You can also specify an output filename and AI model:

```bash
translate-pptx my_slides.pptx german my_translated_slides.pptx gpt-4o
```

### Command Line Options

```bash
translate-pptx <input.pptx> <target_language> [output.pptx] [model]
```

**Arguments:**
- `input.pptx` - Input PowerPoint file to translate (required)
- `target_language` - Target language (required, e.g., german, french, spanish, korean, japanese)
- `output.pptx` - Output file name (optional, auto-generated if not specified)
- `model` - AI model to use (optional, default: gpt-4o-2024-11-20)

### Examples

**Basic translation to German:**
```bash
translate-pptx presentation.pptx german
# Creates: presentation_german.pptx
```

**Translation to French with custom output name:**
```bash
translate-pptx slides.pptx french translated_slides.pptx
# Creates: translated_slides.pptx
```

**Translation to Spanish with specific model:**
```bash
translate-pptx deck.pptx spanish output.pptx gpt-4o
# Creates: output.pptx using GPT-4o model
```

**Translation to Korean:**
```bash
translate-pptx meeting.pptx korean
# Creates: meeting_korean.pptx
```

**Translation to Japanese:**
```bash
translate-pptx report.pptx japanese japanese_report.pptx
# Creates: japanese_report.pptx
```

### Getting Help

To see all available options and examples:

```bash
translate-pptx --help
# or
translate-pptx -h
```

### Supported Languages

translate-pptx supports translation to most major languages including:
- **European Languages**: German, French, Spanish, Italian, Portuguese, Dutch, Swedish, Norwegian, Danish, Finnish, Polish, Czech, Hungarian, Romanian, Bulgarian, Croatian, Serbian, Slovenian, Slovak, Lithuanian, Latvian, Estonian
- **Asian Languages**: Korean, Japanese, Chinese (Simplified & Traditional), Thai, Vietnamese, Indonesian, Malay, Filipino, Hindi, Bengali, Urdu, Persian, Arabic, Hebrew, Turkish
- **African Languages**: Swahili, Zulu, Afrikaans, Amharic, Yoruba, Igbo
- **Other Languages**: Russian, Ukrainian, Belarusian, Georgian, Armenian, Azerbaijani, Kazakh, Uzbek, Kyrgyz, Tajik, Turkmen

Under the hood it uses [OpenAI's GPT-4o](https://openai.com/blog/openai-api) to translate the text in the slides and [python-pptx](https://github.com/scanny/python-pptx) to handle the file-format.

## Disclaimer

`translate-pptx` is a research project aiming at streamlining generation of multi-lingual training materials. Under the hood it uses
artificial intelligence / large language models to generate translations. 
Users are responsible to verify the generated content according to good scientific practice.

> [!CAUTION]
> When using OpenAI's LLMs via translate-pptx, you are bound to the terms of service 
> of the respective companies or organizations.
> The slides you specify are transferred to their servers and may be processed and stored there. 
> Make sure to not submit any sensitive, confidential or personal data. Also using these services may cost money.

## Installation

translate-pptx can be installed using pip:

```
pip install translate-pptx
```

## Configuration

### OpenAI API Key Setup

You need to set up your OpenAI API key to use this tool. There are several ways to do this:

#### Option 1: Interactive Input (Recommended)

When you run `translate-pptx` for the first time, it will automatically prompt you to enter your OpenAI API key. The key will be securely input using a password prompt and stored in memory for the current session.

**How it works:**
1. Run any `translate-pptx` command
2. You'll see a prompt asking for your API key
3. Type your API key (it won't be visible on screen for security)
4. Press Enter to confirm
5. The tool will remember your key for the current session

**Example:**
```bash
$ translate-pptx presentation.pptx german
🔑 OpenAI API Key Required
========================================
You need an OpenAI API key to use translate-pptx.
Get your API key from: https://platform.openai.com/api-keys

Enter your OpenAI API key: ********
✅ API key set successfully
```

#### Option 2: Environment Variable

Set the `OPENAI_API_KEY` environment variable in your shell:

```bash
# Linux/macOS
export OPENAI_API_KEY=sk-your_actual_api_key_here

# Windows (Command Prompt)
set OPENAI_API_KEY=sk-your_actual_api_key_here

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-your_actual_api_key_here"
```

**To make it permanent:**
```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
echo 'export OPENAI_API_KEY=sk-your_actual_api_key_here' >> ~/.bashrc
source ~/.bashrc
```

#### Option 3: Using a .env file

1. Create a `.env` file in your project directory:
```bash
# Create the .env file
touch .env

# Edit the .env file and add your API key
nano .env
```

2. Add your OpenAI API key to the `.env` file:
```
OPENAI_API_KEY=sk-your_actual_api_key_here
```

> [!NOTE]
> The interactive input method is now the default and most user-friendly approach. Your API key is never stored on disk unless you explicitly create a .env file.

### Getting Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Give it a name (e.g., "translate-pptx")
5. Copy the generated key (starts with `sk-`)
6. Use this key with translate-pptx

> [!CAUTION]
> Keep your API key secure and never share it publicly. The key gives access to your OpenAI account and can incur charges.

## Troubleshooting

### Common Issues

**"OpenAI API key is required" error:**
- Make sure you've entered your API key when prompted
- Check that your API key starts with `sk-`
- Verify your API key is valid at [OpenAI Platform](https://platform.openai.com/api-keys)

**"AuthenticationError: Incorrect API key" error:**
- Your API key is invalid or expired
- Generate a new API key at [OpenAI Platform](https://platform.openai.com/api-keys)
- Make sure you're copying the entire key including the `sk-` prefix

**"File not found" error:**
- Check that your PowerPoint file exists in the current directory
- Use the full path if the file is in a different location
- Make sure the file has a `.pptx` extension

**Translation quality issues:**
- Try using a different target language
- Check that your source text is clear and well-formatted
- Consider using the `gpt-4o` model for better quality

### Performance Tips

- **Large files**: For presentations with many slides, the translation may take several minutes
- **Internet connection**: Ensure you have a stable internet connection for API calls
- **API limits**: Be aware of OpenAI's rate limits and usage quotas

## FAQ

**Q: Can I translate to any language?**
A: Yes! translate-pptx supports most major languages including European, Asian, African, and other world languages.

**Q: How much does it cost?**
A: Costs depend on your OpenAI API usage. Check [OpenAI's pricing page](https://openai.com/pricing) for current rates.

**Q: Is my data secure?**
A: Your PowerPoint files are sent to OpenAI's servers for translation. Avoid uploading sensitive or confidential documents.

**Q: Can I use this offline?**
A: No, translate-pptx requires an internet connection to communicate with OpenAI's API.

**Q: What if the translation isn't perfect?**
A: AI translations may contain errors. Always review and edit the translated content before using it in important presentations.

## Contributing

Feedback and contributions are welcome! Just open an issue and let's discuss before you send a pull request.

## Acknowledgements

We acknowledge the financial support by the Federal Ministry of Education and Research of Germany and by Sächsische Staatsministerium für Wissenschaft, Kultur und Tourismus in the programme Center of Excellence for AI-research „Center for Scalable Data Analytics and Artificial Intelligence Dresden/Leipzig", project identification number: ScaDS.AI
