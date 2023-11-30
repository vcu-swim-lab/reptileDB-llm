import csv
import re
import chardet
import pandas as pd
import logging
from chains.zero_shot import TraitsExtractor
from chains.zero_shot_v2 import TraitsExtractorV2
from chains.zero_shot_v3 import TraitsExtractorV3
from langdetect import detect as lang_detect

from argparse import ArgumentParser
from os import getenv


def detect_encoding(file_path):
    """Detect the encoding of a given file."""
    try:
        with open(file_path, 'rb') as file:
            result = chardet.detect(file.read())
            return result['encoding']
    except Exception as e:
        logging.error(f"Error detecting file encoding: {e}")
        raise


def process_line(line, traits_extractor, version):
    """Process a single line of species data."""
    if not line.strip() or lang_detect(line) != 'en':
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

    counts = count_categories_for_family(species_data, "Colubridae")
    print(f"Category counts for 'Colubridae': {counts}")

    output_filename = 'family_categories.csv'
    write_term_counts_to_csv("Colubridae", counts, output_filename)

    print(species_data)

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


def main(file_path, version):
    """Main function to process species data."""
    getenv("OPENAI_API_KEY")
    if version == 1:
        traits_extractor = TraitsExtractor()
    elif version == 2:
        traits_extractor = TraitsExtractorV2()
    elif version == 3:
        traits_extractor = TraitsExtractorV3()
    else:
        raise ValueError("Invalid version specified. Choose 1,2, or 3.")

    output_filename = f'extracted_traits_v{version}.csv'

    file_encoding = detect_encoding(file_path)

    with open(file_path, 'r', encoding=file_encoding) as file:
        species_data, trait_categories = process_species_data(file, traits_extractor, version)
        df = write_to_csv(species_data, trait_categories, output_filename, version)
        df.to_csv(output_filename, index=False, encoding='utf-8')
        print(f"Output saved to {output_filename}")


if __name__ == "__main__":
    parser = ArgumentParser(description="Process reptile species data.")
    parser.add_argument('file', type=str, help='Path to the input file')
    parser.add_argument('version', type=int, choices=[1, 2, 3], help='Version of the Traits Extractor (1, 2, or 3)')
    args = parser.parse_args()
    main(args.file, args.version)
