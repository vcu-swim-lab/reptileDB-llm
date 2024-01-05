import csv
from collections import defaultdict


class ReptileTraits:

    @staticmethod
    def to_csv(output_text, family):
        # Making the new csv file
        with open('traits.csv', 'w', newline='') as new_file:
            fieldnames = ['trait', 'attribute', 'family']
            csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter='|')

            # Adding column headers
            csv_writer.writeheader()

            # Going through every line in the output text
            for line in output_text:
                holder = line.split('|')

                # Remove the white space
                holder = [part.strip() for part in holder]

                # Remove the number at the beginning of the trait
                trait_parts = holder[0].split('. ', 1)
                if len(trait_parts) > 1:
                    holder[0] = trait_parts[1]

                # Make sure the trait is true and then add it to the csv file
                if holder[2] == 'True':
                    csv_writer.writerow(
                        {'trait': holder[0], 'attribute': holder[1], 'family': family})

        # automatically updating the stats csv file after making a new csv file
        ReptileTraits.get_stats()

    @staticmethod
    def get_stats():
        traits_file = 'traits.csv'
        count_file_path = 'trait_counts.csv'

        counts_dict = defaultdict(int)

        try:
            with open(count_file_path, 'r', newline='') as count_file:
                csv_reader = csv.reader(count_file, delimiter='|')
                next(csv_reader, None)
                for row in csv_reader:
                    if len(row) >= 4:
                        counts_dict[(row[0], row[1], row[2])] += int(row[3])
        except FileNotFoundError:
            pass

        with open(traits_file, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='|')
            next(csv_reader, None)
            for line in csv_reader:
                if len(line) >= 3:
                    counts_dict[(line[2], line[0], line[1])] += 1

        with open(count_file_path, 'w', newline='') as count_file:
            csv_writer = csv.writer(count_file, delimiter='|')
            csv_writer.writerow(['family', 'trait', 'attribute', 'count'])
            for (fam, trait, attr), count in counts_dict.items():
                csv_writer.writerow([fam, trait, attr, count])



ReptileTraits.to_csv(["10. caudal annuli | 10-15 | True | as this is the number of caudal annuli (quantitative trait).",
                      "11. dorsal segments/midbody annulus | 14-17 | True | as this is a quantitative trait (quantitative trait).",
                      "2. Sauria | no adjective | False | as this is an order.", "16. intersegmental raphes | light | True | as it is a color (color).", "16. intersegmental raphes | light | True | as it is a color (color)."], "Amphisbaenidae")
