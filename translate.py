import logging
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator


def is_english(line):
    """Determine if the description is English."""
    try:
        return detect(line.strip()) == 'en'
    except LangDetectException:
        logging.error("Error detecting language.")
        return False


def translate_to_english(text):
    """Translate the given text to English using Google Translate."""
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        return translated
    except Exception as e:
        logging.error(f"Error translating text: {e}")
        return None


if __name__ == "__main__":
    text = "El hombre tiene tres hijos."

    if not is_english(text):
        translation = translate_to_english(text)
        if translation:
            print(translation)
        else:
            logging.error("Failed to translate text.")
