import csv
from collections import defaultdict


class ReptileTraits:

    @staticmethod
    def to_csv(output_text, family):
        traits_file = f'traits_{family}.csv'
        with open(traits_file, 'w', newline='') as new_file:
            fieldnames = ['trait', 'attribute', 'family']
            csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)

            csv_writer.writeheader()

            for item in output_text:
                lines = item.split('\n')
                for line in lines:
                    holder = line.split('|')
                    holder = [part.strip() for part in holder]

                    if len(holder) < 3:
                        continue

                    trait_parts = holder[0].split('. ', 1)
                    if len(trait_parts) > 1:
                        holder[0] = trait_parts[1]

                    if holder[2] == 'True':
                        csv_writer.writerow({'trait': holder[0], 'attribute': holder[1], 'family': family})

        ReptileTraits.get_stats(family)

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
                    if len(row) >= 4:
                        counts_dict[(row[0], row[1], row[2])] += int(row[3])
        except FileNotFoundError:
            pass

        with open(traits_file, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader, None)
            for line in csv_reader:
                if len(line) >= 3:
                    counts_dict[(line[2], line[0], line[1])] += 1

        with open(count_file_path, 'w', newline='') as count_file:
            csv_writer = csv.writer(count_file)
            csv_writer.writerow(['family', 'trait', 'attribute', 'count'])
            for (fam, trait, attr), count in counts_dict.items():
                csv_writer.writerow([fam, trait, attr, count])