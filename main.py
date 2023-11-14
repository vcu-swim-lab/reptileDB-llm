import csv
import re
import chardet
import pandas as pd
from chains.zero_shot import TraitsExtractor
from chains.zero_shot_v2 import TraitsExtractorV2
from chains.zero_shot_v3 import TraitsExtractorV3

from argparse import ArgumentParser
from os import getenv


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        return result['encoding']


def process_species_data(file, traits_extractor, version):
    char_or_cat = 'Characteristics' if version in [1, 2] else 'Categories'
    trait_categories = set()
    species_data = []

    with file as file_stream:
        for line in file_stream:
            if not line.strip():
                continue
            species, diagnosis, characteristics = extract_species_info(line, traits_extractor, version)
            if species and diagnosis:
                if isinstance(characteristics, str):
                    characteristics = [(characteristics, '')]

                if characteristics:
                    trait_categories.update({trait for _, trait in characteristics})

            species_data.append({'Species': species, char_or_cat: characteristics})
    return species_data, trait_categories


def extract_species_info(line, traits_extractor, version):
    elements = line.split()
    genus = elements[0]
    epithet = elements[1]
    species = genus + " " + epithet
    order = elements[2]
    family = elements[3]
    abstract = ' '.join(elements[4:])

    categorized_traits = traits_extractor.get_categorized_traits().run(f"{species}: {abstract}")

    if version == 3:
        categories_split = categorized_traits.split()
        categories_list = categories_split[1:]
        categories = ' '.join(categories_list)
        print(f"{species}: {categories}")
        return species, abstract, categories

    match = re.match(r"([\w\s-]+): (.+)", categorized_traits)
    if match:
        characteristics = re.findall(r"([\w\s-]+) <([\w\s-]+)>", match.group(2))
        return species, abstract, characteristics
    return species, abstract, []


def write_to_csv(species_data, trait_categories, filename):
    fieldnames = ['Species'] + sorted(trait_categories)
    rows = [create_csv_row(data) for data in species_data]

    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return pd.DataFrame(rows)


def create_csv_row(data):
    row = {'Species': data['Species']}
    for characteristic, trait in data['Characteristics']:
        row[trait] = characteristic
    return row


def main(file_path, version):
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
        df = write_to_csv(species_data, trait_categories, output_filename)
        df.to_csv(output_filename, index=False, encoding='utf-8')
        print(f"Output saved to {output_filename}")


if __name__ == "__main__":
    parser = ArgumentParser(description="Process reptile species data.")
    parser.add_argument('file', type=str, help='Path to the input file')
    parser.add_argument('version', type=int, choices=[1, 2, 3], help='Version of the Traits Extractor (1, 2, or 3)')
    args = parser.parse_args()
    main(args.file, args.version)