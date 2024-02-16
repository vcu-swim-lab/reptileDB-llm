import csv
import logging
import os
import pandas as pd
import chardet


def detect_encoding(file_path):
    """Detect the encoding of a given file."""
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return None

    try:
        with open(file_path, 'rb') as file:
            result = chardet.detect(file.read())
            return result['encoding']
    except Exception as e:
        logging.error(f"Error detecting file encoding: {e}")
        raise


class ReptileTraits:

    @staticmethod
    def to_csv(output_text, family):
        traits_file = f'traits_{family.lower()}.csv'
        data = {}

        for species_name, item in output_text:
            lines = item.split('\n')
            for line in lines:
                holder = line.split('|')
                holder = [part.strip().lower() for part in holder]

                if len(holder) == 4 and holder[2].lower() == 'true':
                    trait = holder[0].split('. ', 1)[-1]
                    attribute = holder[1]
                    if species_name not in data:
                        data[species_name] = {}
                    data[species_name][trait] = attribute

        all_traits = set()
        for traits in data.values():
            all_traits.update(traits.keys())
        headers = ['species'] + sorted(all_traits)

        with open(traits_file, 'w', newline='', encoding='utf-8') as new_file:
            csv_writer = csv.DictWriter(new_file, fieldnames=headers)
            csv_writer.writeheader()

            for species, traits in data.items():
                row = {'species': species}
                row.update(traits)
                csv_writer.writerow(row)

        ReptileTraits.get_stats(family.lower())

    @staticmethod
    def get_stats(family):
        traits_file = f'traits_{family.lower()}.csv'
        counts_file = f'as_is_trait_counts_{family.lower()}.csv'

        df = pd.read_csv(traits_file)

        trait_counts = {}

        for trait in df.columns[1:]:
            trait_counts[trait] = df[trait].notna().sum()

        trait_counts_df = pd.DataFrame(list(trait_counts.items()), columns=['trait', 'count'])

        trait_counts_df.to_csv(counts_file, index=False)