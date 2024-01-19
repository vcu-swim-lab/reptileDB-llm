import csv
import logging
import os
from collections import defaultdict

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
        if not os.path.exists(traits_file):
            with open(traits_file, 'w', newline='', encoding='utf-8') as file:
                file.write('trait,attribute,family\n')

        encoding = detect_encoding(traits_file)

        with open(traits_file, 'a', newline='', encoding='utf-8') as new_file:
            fieldnames = ['trait', 'attribute', 'family']
            csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)

            if os.stat(traits_file).st_size == 0:
                csv_writer.writeheader()

            for item in output_text:
                lines = item.split('\n')
                for line in lines:
                    holder = line.split('|')
                    holder = [part.strip().lower() for part in holder]

                    if len(holder) < 3:
                        continue

                    trait_parts = holder[0].split('. ', 1)
                    if len(trait_parts) > 1:
                        holder[0] = trait_parts[1]

                    if holder[2] == 'true':
                        csv_writer.writerow({'trait': holder[0], 'attribute': holder[1], 'family': family.lower()})

        # ReptileTraits.get_stats(family.lower())

    @staticmethod
    def get_stats(family):
        traits_file = f'traits_{family.lower()}.csv'
        count_file_path = f'trait_counts_{family.lower()}.csv'
        counts_dict = defaultdict(int)

        encoding = detect_encoding(traits_file)

        try:
            with open(count_file_path, 'r', newline='', encoding=encoding) as count_file:
                csv_reader = csv.reader(count_file)
                next(csv_reader, None)
                for row in csv_reader:
                    if len(row) >= 3:
                        key = (row[0].lower(), row[1].lower())
                        counts_dict[key] = int(row[2])
        except FileNotFoundError:
            pass

        with open(traits_file, 'r', newline='', encoding=encoding) as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader, None)
            for line in csv_reader:
                if len(line) >= 3:
                    key = (line[2].lower(), line[0].lower())
                    counts_dict[key] += 1

        with open(count_file_path, 'w', newline='', encoding=encoding) as count_file:
            csv_writer = csv.writer(count_file)
            csv_writer.writerow(['family', 'trait', 'count'])
            for (family, trait), count in counts_dict.items():
                csv_writer.writerow([family, trait, count])


# need to test
"""
    @staticmethod
    def get_stats(family):
        traits_file = f'traits_{family.lower()}.csv'
        count_file_path = f'trait_counts_{family.lower()}.csv'
        counts_dict = defaultdict(int)

        encoding = detect_encoding(traits_file)

        try:
            with open(count_file_path, 'r', newline='', encoding=encoding) as count_file:
                csv_reader = csv.reader(count_file)
                next(csv_reader, None)
                for row in csv_reader:
                    if len(row) >= 3:
                        key = (row[0].lower(), row[1].lower(), row[2].lower())
                        counts_dict[key] = int(row[2])
        except FileNotFoundError:
            pass

        with open(traits_file, 'r', newline='', encoding=encoding) as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader, None)
            for line in csv_reader:
                if len(line) >= 3:
                    key = (line[2].lower(), line[0].lower(), line[1].lower())
                    counts_dict[key] += 1

        with open(count_file_path, 'w', newline='', encoding=encoding) as count_file:
            csv_writer = csv.writer(count_file)
            csv_writer.writerow(['family', 'trait', 'attribute', 'count'])
            for (family, trait, attribute), count in counts_dict.items():
                csv_writer.writerow([family, trait, attribute, count])"""
