import csv

class ReptileTraits:

    @staticmethod
    def to_csv(output_text, family):
        # Making the new csv file
        with open('traits.csv', 'w', newline='') as new_file:
            fieldnames = ['species', 'trait', 'attribute', 'family']
            csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter='|')

            # Adding column headers
            csv_writer.writeheader()

            # Going through every line in the output text
            for line in output_text:
                holder = line.split('|')

                # Remove the white space
                holder = [part.strip() for part in holder]

                # Make sure the trait is true and then add it to the csv file
                if holder[2] == 'True':
                    csv_writer.writerow({'species': holder[0], 'trait': holder[1], 'attribute': holder[2], 'family': family})

        # automatically updating the stats csv file after making a new csv file
        ReptileTraits.get_stats()

    @staticmethod
    def get_stats():
        traits_file = 'traits.csv'
        # Creating/append new csv file for the trait counts by family
        with open('trait_counts.csv', 'a+', newline='') as count_file:
            fieldnames = ['family', 'trait', 'count']
            csv_writer = csv.writer(count_file, delimiter='|')  # Use csv.writer instead of csv.DictWriter

            # Put the data already on the file into a list (if file exists already)
            existing_data = list(csv.reader(count_file, delimiter='|'))  # Specify the delimiter

            # Adding column headers if the file is empty
            if not existing_data:
                csv_writer.writerow(fieldnames)

            # Create a dictionary to store counts for each family and trait
            counts_dict = {(row[0], row[1]): int(row[2]) for row in existing_data[1:]}  # Skip the first row

            # To open and read the original csv file
            with open(traits_file, 'r') as csv_file:
                # Reading the OG file
                csv_reader = csv.reader(csv_file, delimiter='|')  # Specify the delimiter
                next(csv_reader)  # Skip the header

                # Going through each line in the OG file
                for line in csv_reader:
                    # Check if the line has enough elements
                    if len(line) >= 4:
                        # Storing the current lines family and trait
                        fam = line[3]
                        trait = line[1]

                        # Update the counts in the dictionary
                        counts_dict[(fam, trait)] = counts_dict.get((fam, trait), 0) + 1

            # Write the updated counts back to the CSV file
            count_file.seek(0)  # Move the file cursor to the beginning
            count_file.truncate()  # Clear the file content

            csv_writer.writerow(fieldnames)  # Rewrite the header
            for (fam, trait), count in counts_dict.items():
                csv_writer.writerow([fam, trait, count])

# Example usage:
output_text = ["Amphisbaena innocens | no attribute | False | family1", "Sauria | no attribute | True | family2", "Sauria | no attribute | True | family2"]
ReptileTraits.to_csv(output_text)