from googletrans import Translator, LANGUAGES

# Initialize the Translator
translator = Translator()

# Function to get language code from the language name
def get_language_code(language_name):
    """
    Returns the language code for a given language name.
    
    Args:
    language_name (str): The name of the language (e.g., 'English', 'Spanish').
    
    Returns:
    str: Corresponding language code, or None if not found.
    """
    # Convert language names to lower case and find the code
    language_name = language_name.lower()
    for code, name in LANGUAGES.items():
        if name.lower() == language_name:
            return code
    return None

# Function to translate the text
def translate_text(text, src_lang_name='auto', dest_lang_name='English'):
    """
    Translates text from the source language to the destination language.
    
    Args:
    text (str): The text to translate.
    src_lang_name (str): The source language name (default is 'auto').
    dest_lang_name (str): The target language name (default is 'English').
    
    Returns:
    str: Translated text or an error message.
    """
    # Get language codes from language names
    src_lang_code = get_language_code(src_lang_name) if src_lang_name != 'auto' else 'auto'
    dest_lang_code = get_language_code(dest_lang_name)

    if dest_lang_code is None:
        return f"Error: Destination language '{dest_lang_name}' not found."
    
    try:
        # Perform translation
        translated = translator.translate(text, src=src_lang_code, dest=dest_lang_code)
        return translated.text
    except Exception as e:
        return f"Error: {str(e)}"

# Take user input for text and language names
text = input("Enter the text you want to translate: ")
src_lang_name = input("Enter the source language (default is 'auto' for automatic detection): ") or 'auto'
dest_lang_name = input("Enter the target language (default is 'English'): ") or 'English'

# Translate and display the result
translated_text = translate_text(text, src_lang_name, dest_lang_name)
print(f"Original Text: {text}")
print(f"Translated Text: {translated_text}")
