import logging
from argparse import ArgumentParser
from os import getenv
import chardet
from io import StringIO

import pandas as pd
from langdetect import detect, LangDetectException

from chains.GPT.species_utils import process_species_data, write_to_csv
from chains.GPT.zero_shot import TraitsExtractor
from chains.GPT.zero_shot_v2 import TraitsExtractorV2
from chains.GPT.zero_shot_v3 import TraitsExtractorV3
from chains.LLaMA2.fewshot import TraitsExtractorV4, parse_traits
from chains.GPT.fewshot_gpt import TraitsExtractorGPT
from reptile_traits import ReptileTraits
from prompts.LLaMA2.NER_prompt2 import prompt
from prompts.LLaMA2.summarize_prompt_llama import step_two



def detect_encoding(file_path):
    """Detect the encoding of a given file."""
    try:
        with open(file_path, 'rb') as file:
            result = chardet.detect(file.read())
            return result['encoding']
    except Exception as e:
        logging.error(f"Error detecting file encoding: {e}")
        raise


def is_english(line):
    """Determine if the description is English."""
    try:
        return detect(line.strip()) == 'en'
    except LangDetectException:
        return False


def main(file_path, family_name, version):
    """Main function to process species data."""
    global traits_extractor
    getenv("OPENAI_API_KEY")

    if version not in [1, 2, 3, 4, 5]:
        raise ValueError("Invalid version specified. Choose 1, 2, 3, 4, or 5.")

    file_encoding = detect_encoding(file_path)

    if version == 1:
        traits_extractor = TraitsExtractor()
    elif version == 2:
        traits_extractor = TraitsExtractorV2()
    elif version == 3:
        traits_extractor = TraitsExtractorV3()
    elif version == 4:
        traits_extractor = TraitsExtractorV4()
    elif version == 5:
        traits_extractor = TraitsExtractorGPT(model_name="gpt-4")

    with open(file_path, 'r', encoding=file_encoding) as file:
        if version in [1, 2, 3]:
            output_filename = f'extracted_traits_v{version}.csv'
            species_data, trait_categories = process_species_data(file, traits_extractor, version)
            df = write_to_csv(species_data, trait_categories, output_filename, version)
            df.to_csv(output_filename, index=False, encoding='utf-8')
            print(f"Output saved to {output_filename}")

        elif version in [4, 5]:
            output_text = []
            line_number = 1

            for line in file:
                if not is_english(line):
                    print(f"Skipping non-English line #{line_number}")
                    line_number += 1
                    continue

                species_name = ' '.join(line.strip().split()[:2])
                try:
                    if version == 4:
                        result, _ = traits_extractor.run_with_retries(line, prompt)
                    else:
                        result = traits_extractor.get(diagnosis=line)

                    print(f"Line #{line_number}\n{result}")
                    output_text.append((species_name, result))
                except Exception as e:
                    print(f"Error processing line #{line_number}: {e}")
                finally:
                    line_number += 1

            ReptileTraits.to_csv(output_text, family_name)

            df = pd.read_csv(f'as_is_trait_counts_{family_name.lower()}.csv')
            output = StringIO()
            df.to_csv(output, index=False)
            data_string = output.getvalue()
            synonymous_characteristics = traits_extractor.final_step(data_string, step_two)
            print(f"CHARACTERISTICS: {data_string}")
            print(f"SYN CHARACTERISTICS: {synonymous_characteristics}")
            parse_traits(family_name, synonymous_characteristics)
            

if __name__ == "__main__":
    parser = ArgumentParser(description="Process reptile species data.")
    parser.add_argument('file', type=str, help='Path to the input file')
    parser.add_argument('family', type=str, help='Family name of the species')
    parser.add_argument('version', type=int, choices=[1, 2, 3, 4, 5],
                        help='Version of the Traits Extractor (1, 2, 3, 4, or 5)')
    args = parser.parse_args()
    main(args.file, args.family, args.version)
