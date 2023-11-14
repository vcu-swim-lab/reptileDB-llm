import csv
import re
import chardet
import pandas as pd
from chains.zero_shot import TraitsExtractor
from chains.zero_shot_v2 import TraitsExtractorV2
from chains.zero_shot_v3 import TraitsExtractorV3
from langdetect import detect as lang_detect

from argparse import ArgumentParser
from os import getenv


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        return result['encoding']


def process_line(line, traits_extractor, version):
    if not line.strip() or lang_detect(line) != 'en':
        return None, None

    species, diagnosis, characteristics = extract_species_info(line, traits_extractor, version)

    if species and diagnosis:
        if isinstance(characteristics, str):
            characteristics = [(characteristics, '')]

        return {'Species': species, 'Characteristics' if version in [1, 2] else 'Categories': characteristics}, set(
            trait for _, trait in characteristics)

    return None, None


def process_species_data(file, traits_extractor, version):
    trait_categories = set()
    species_data = []

    with file as file_stream:
        for line in file_stream:
            data, traits = process_line(line, traits_extractor, version)
            if data:
                trait_categories.update(traits)
                species_data.append(data)

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
        return parse_categories_v3(species, abstract, categorized_traits)
    else:
        return parse_characteristics_v1v2(species, abstract, categorized_traits)


def parse_characteristics_v1v2(species, abstract, categorized_traits):
    match = re.match(r"([\w\s-]+): (.+)", categorized_traits)
    if match:
        characteristics = re.findall(r"([\w\s-]+) <([\w\s-]+)>", match.group(2))
        return species, abstract, characteristics
    return species, abstract, []


def parse_categories_v3(species, abstract, categorized_traits):
    categories_split = categorized_traits.split()
    categories_list = categories_split[1:]
    categories = ' '.join(categories_list)
    return species, abstract, categories


def write_to_csv(species_data, trait_categories, filename, version):
    fieldnames = ['Species'] + sorted(trait_categories)
    rows = [create_csv_row(data, version) for data in species_data]

    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return pd.DataFrame(rows)


def create_csv_row(data, version):
    char_or_cat = 'Characteristics' if version in [1, 2] else 'Categories'
    row = {'Species': data['Species']}
    for characteristic, trait in data[char_or_cat]:
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
        df = write_to_csv(species_data, trait_categories, output_filename, version)
        df.to_csv(output_filename, index=False, encoding='utf-8')
        print(f"Output saved to {output_filename}")


if __name__ == "__main__":
    parser = ArgumentParser(description="Process reptile species data.")
    parser.add_argument('file', type=str, help='Path to the input file')
    parser.add_argument('version', type=int, choices=[1, 2, 3], help='Version of the Traits Extractor (1, 2, or 3)')
    args = parser.parse_args()
    main(args.file, args.version)
