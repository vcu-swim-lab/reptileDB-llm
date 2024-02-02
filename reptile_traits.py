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

        with open(traits_file, 'w', newline='', encoding='utf-8') as new_file:
            fieldnames = ['species', 'trait', 'attribute']
            csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
            csv_writer.writeheader()

            species_name = ""

            for item in output_text:
                lines = item.split('\n')
                for line in lines:
                    holder = line.split('|')
                    holder = [part.strip().lower() for part in holder]

                    if line.startswith('1.') and len(holder) >= 4:
                        species_name = holder[0].split('. ', 1)[1]

                    elif len(holder) == 4 and holder[2].lower() == 'true':
                        trait = holder[0]
                        if '.' in trait:
                            trait = trait.split('. ', 1)[-1]
                        attribute = holder[1]
                        csv_writer.writerow({
                            'species': species_name,
                            'trait': trait,
                            'attribute': attribute,
                        })

        ReptileTraits.get_stats(family.lower())

    @staticmethod
    def to_csv_2(output_text, family):
        traits_file = f'v2traits_{family.lower()}.csv'

        species_traits = {}

        for item in output_text:
            lines = item.split('\n')
            species_name = ""
            for line in lines:
                holder = line.split('|')
                holder = [part.strip().lower() for part in holder]

                if line.startswith('1.') and len(holder) >= 4:
                    species_name = holder[0].split('. ', 1)[1]
                    species_traits[species_name] = []

                elif len(holder) == 4 and holder[2].lower() == 'true':
                    if species_name:
                        trait = holder[0]
                        if '.' in trait:
                            trait = trait.split('. ', 1)[-1]
                        attribute = holder[1]

                        if species_name in species_traits:
                            species_traits[species_name].append(f'{trait} {attribute}')
                        else:
                            print(f"Species name not initialized: '{species_name}'")
                    else:
                        print("Encountered a trait line without a preceding species name.")

        with open(traits_file, 'w', newline='', encoding='utf-8') as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow(['species', 'traits'])

            for species, traits in species_traits.items():
                row = [species] + [', '.join(traits)]
                csv_writer.writerow(row)

    @staticmethod
    def get_stats(family):
        traits_file = f'traits_{family.lower()}.csv'
        counts_file = f'as_is_trait_counts_{family.lower()}.csv'

        df = pd.read_csv(traits_file)

        trait_counts = df.groupby('trait').size().reset_index(name='count')
        trait_counts.to_csv(counts_file, index=False)

