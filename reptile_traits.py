import csv
from collections import defaultdict


class ReptileTraits:

    @staticmethod
    def to_csv(output_text, family):
        traits_file = f'traits_{family.lower()}.csv'
        with open(traits_file, 'w', newline='') as new_file:
            fieldnames = ['trait', 'attribute', 'family']
            csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)

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

        ReptileTraits.get_stats(family.lower())

    @staticmethod
    def get_stats(family):
        traits_file = f'traits_{family}.csv'
        count_file_path = f'trait_counts_{family}.csv'

        counts_dict = defaultdict(int)

        try:
            with open(count_file_path, 'r', newline='') as count_file:
                csv_reader = csv.reader(count_file)
                next(csv_reader, None)
                for row in csv_reader:
                    if len(row) >= 3:
                        key = (row[0].lower(), row[1].lower())
                        counts_dict[key] = int(row[2])
        except FileNotFoundError:
            pass

        with open(traits_file, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader, None)
            for line in csv_reader:
                if len(line) >= 3:
                    key = (line[2].lower(), line[0].lower())
                    counts_dict[key] += 1

        with open(count_file_path, 'w', newline='') as count_file:
            csv_writer = csv.writer(count_file)
            csv_writer.writerow(['family', 'trait', 'count'])
            for (family, trait), count in counts_dict.items():
                csv_writer.writerow([family, trait, count])
