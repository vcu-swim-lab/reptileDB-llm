import io
import csv
import re
import pandas as pd
from zero_shot import TraitsExtractor
from zero_shot_v2 import TraitsExtractorV2
from argparse import ArgumentParser
from os import getenv


def process_species_data(file, traits_extractor):
    trait_categories = set()
    species_data = []

    with file as file_stream:
        for line in file_stream:
            species, diagnosis, characteristics = extract_species_info(line, traits_extractor)
            if species and characteristics:
                trait_categories.update({trait for _, trait in characteristics})
                species_data.append({'Species': species, 'Characteristics': characteristics})

    return species_data, trait_categories


def extract_species_info(line, traits_extractor):
    input_line = line.split()
    species = ' '.join(input_line[0:2])
    diagnosis = ' '.join(input_line[2:])
    categorized_traits = traits_extractor.get_categorized_traits().run(f"{species}: {diagnosis}")

    match = re.match(r"([\w\s-]+): (.+)", categorized_traits)
    if match:
        characteristics = re.findall(r"([\w\s-]+) <([\w\s-]+)>", match.group(2))
        return species, diagnosis, characteristics
    return species, diagnosis, []


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
    else:
        raise ValueError("Invalid version specified. Choose 1 or 2.")
    output_filename = f'extracted_traits_v{version}.csv'

    with open(file_path, 'r', encoding='utf-8') as file:
        species_data, trait_categories = process_species_data(file, traits_extractor)
        df = write_to_csv(species_data, trait_categories, output_filename)
        df.to_csv(output_filename, index=False, encoding='utf-8')
        print(f"Output saved to {output_filename}")


if __name__ == "__main__":
    parser = ArgumentParser(description="Process reptile species data.")
    parser.add_argument('file', type=str, help='Path to the input file')
    parser.add_argument('version', type=int, choices=[1, 2], help='Version of the Traits Extractor (1 or 2)')
    args = parser.parse_args()
    main(args.file, args.version)
