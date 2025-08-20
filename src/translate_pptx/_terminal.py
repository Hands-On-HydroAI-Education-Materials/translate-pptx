def command_line_interface(argv=None):
    """Command-line interface for the translate_pptx package."""
    import sys
    import os

    from ._pptx import extract_text_from_slides, replace_text_in_slides
    from ._translation import translate_data_structure_of_texts_recursive
    from ._endpoints import prompt_openai, prompt_nop, get_api_key_from_user

    # Read config from terminal arguments
    if argv is None:
        argv = sys.argv

    # Check for help option
    if len(argv) == 1 or "--help" in argv or "-h" in argv:
        print("translate-pptx - Translate PowerPoint presentations using AI")
        print("=" * 55)
        print()
        print("Usage:")
        print("  translate-pptx <input.pptx> <target_language> [output.pptx] [model]")
        print()
        print("Arguments:")
        print("  input.pptx      Input PowerPoint file to translate")
        print("  target_language Target language (e.g., german, french, spanish)")
        print("  output.pptx     Output file name (optional)")
        print("  model          AI model to use (optional, default: gpt-4o)")
        print()
        print("Examples:")
        print("  translate-pptx presentation.pptx german")
        print("  translate-pptx slides.pptx french translated_slides.pptx")
        print("  translate-pptx deck.pptx spanish output.pptx gpt-4o")
        print()
        print("Note: You will be prompted to enter your OpenAI API key on first use.")
        return

    # Check if we have the minimum required arguments
    if len(argv) < 3:
        print("Error: Insufficient arguments.")
        print("Use 'translate-pptx --help' for usage information.")
        return

    input_pptx = argv[1]
    target_language = argv[2]
    if len(argv) > 3:
        output_pptx = argv[3]
    else:
        counter = 0
        suffix = ""
        while True:
            output_pptx = input_pptx.replace(".pptx", f"_{target_language}{suffix}.pptx")
            if os.path.exists(output_pptx):
                counter += 1
                suffix = f"_{counter}"
            else:
                break
    if len(argv) > 4:
        llm_name = argv[4]
    else:
        llm_name = "gpt-4o-2024-11-20"

    if llm_name == "nop":
        prompt_function = prompt_nop
    elif "gpt-4o" in llm_name:
        # Get API key from user if using OpenAI
        api_key = get_api_key_from_user()
        # Create a wrapper function that passes the API key
        def prompt_with_api_key(message):
            return prompt_openai(message, llm_name, api_key)
        prompt_function = prompt_with_api_key
    else:
        raise ValueError(f"Unknown model: {llm_name}")

    # Extract text
    texts = extract_text_from_slides(input_pptx)

    # Translate text
    translated_texts = translate_data_structure_of_texts_recursive(texts, prompt_function, target_language)

    # Replace text
    replace_text_in_slides(input_pptx, translated_texts, output_pptx)

    print(f"Translated presentation saved to {output_pptx}")
