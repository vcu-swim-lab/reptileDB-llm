import csv
import re
from io import StringIO

import chardet
import pandas as pd
import logging

from chains.GPT.zero_shot import TraitsExtractor
from chains.GPT.zero_shot_v2 import TraitsExtractorV2
from chains.GPT.zero_shot_v3 import TraitsExtractorV3
from chains.LLaMA2.fewshot import TraitsExtractorV4, parse_traits
from chains.GPT.fewshot_gpt import TraitsExtractorGPT
from langdetect import detect as lang_detect
from googletrans import Translator

from argparse import ArgumentParser
from os import getenv

from reptile_traits import ReptileTraits
from prompts.LLaMA2.NER_prompt import prompt
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


def translate(non_english):
    translator = Translator()
    translation = translator.translate(non_english, dest='en')
    return translation.text


def process_line(line, traits_extractor, version):
    """Process a single line of species data."""
    if not line.strip():
        return None, None
    try:
        language = lang_detect(line)
    except:
        logging.error(f"Language detection failed for line: {line}")
        return None, None

    if language != 'en':
        try:
            line = translate(line)
        except Exception as e:
            logging.error(f"Error in translation: {e}")
            return None, None

    family, species_info = extract_species_info(line, traits_extractor, version)
    species, diagnosis, characteristics = species_info

    if species and diagnosis:
        if isinstance(characteristics, str):
            characteristics = [(characteristics, '')]

        return {'Species': species, 'Family': family, 'Characteristics' if version in [1, 2] else 'Categories':
            characteristics}, set(trait for _, trait in characteristics)

    return None, None


def count_categories_for_family(species_data, family_name):
    """Count the amount of times a term appears for a given family."""
    category_counts = {}
    for species_dict in species_data:
        if species_dict['Family'] == family_name:
            categories = species_dict['Categories']
            for category_tuple in categories:
                category_list = category_tuple[0].split(', ')
                for category in category_list:
                    if category:
                        category_counts[category] = category_counts.get(category, 0) + 1

    return category_counts


def write_term_counts_to_csv(family_name, category_counts, filename):
    """Write term counts to a csv file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Family', 'Category', 'Count'])
        for category, count in category_counts.items():
            writer.writerow([family_name, category, count])


def process_species_data(file, traits_extractor, version):
    """Adds species data to a dictionary and set for further processing."""
    trait_categories = set()
    species_data = []

    with file as file_stream:
        for line in file_stream:
            data, traits = process_line(line, traits_extractor, version)
            if data:
                trait_categories.update(trait for trait in traits if trait != 'Diagnosis')
                species_data.append(data)

    return species_data, trait_categories


def extract_species_info(line, traits_extractor, version):
    """Extracts specific words from species data."""
    elements = line.split()
    genus = elements[0]
    epithet = elements[1]
    species = genus + " " + epithet
    order = elements[2]
    family = elements[3]
    abstract = ' '.join(elements[4:])

    categorized_traits = traits_extractor.get_categorized_traits().run(f"{species}: {abstract}")
    if version == 3:
        return family, parse_categories_v3(species, abstract, categorized_traits)
    else:
        return family, parse_characteristics_v1v2(species, abstract, categorized_traits)


def parse_characteristics_v1v2(species, abstract, categorized_traits):
    """Extracts characteristics from species data."""
    match = re.match(r"([\w\s-]+): (.+)", categorized_traits)
    if match:
        characteristics = re.findall(r"([\w\s-]+) <([\w\s-]+)>", match.group(2))
        return species, abstract, characteristics
    return species, abstract, []


def parse_categories_v3(species, abstract, categorized_traits):
    """Extracts categories from species data."""
    categories_split = categorized_traits.split()
    categories_list = categories_split[1:]
    categories = ' '.join(categories_list)
    return species, abstract, categories


def write_to_csv(species_data, trait_categories, filename, version):
    """Writes species names, their categories, and their descriptions to a csv file."""
    fieldnames = ['Species'] + sorted(trait_categories)
    rows = [create_csv_row(data, version) for data in species_data]

    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return pd.DataFrame(rows)


def create_csv_row(data, version):
    """Helper method for write_to_csv that creates a csv row."""
    char_or_cat = 'Characteristics' if version in [1, 2] else 'Categories'
    row = {'Species': data['Species']}
    for characteristic, trait in data[char_or_cat]:
        row[trait] = characteristic
    return row


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
                try:
                    if version == 4:
                        result = traits_extractor.process_and_stitch(line, prompt)
                    else:
                        result = traits_extractor.get(diagnosis=line)

                    print(f"Line #{line_number}\n{result}")
                    output_text.append(result)
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
