from dotenv import load_dotenv
import os
from zero_shot import TraitsExtractor
import re
import csv

traits = TraitsExtractor()

load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

if __name__ == "__main__":
    with open("Numbered reptile descriptions.txt", encoding="utf-8") as file:
        with open('extracted_traits.csv', mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Species']

            for line in file:
                diagnosis_index = line.find("Diagnosis")

                if diagnosis_index != -1:
                    species = line[:diagnosis_index].strip().replace("$", "")
                    diagnosis = line[diagnosis_index + len("Diagnosis"):].strip()

                    if species:
                        categorized_traits = traits.get_categorized_traits().run(f"{species}: {diagnosis}")
                        print(categorized_traits)
                        match = re.match(r"([\w\s-]+): (.+)", categorized_traits)

                        if match:
                            species_name = species
                            traits_info = match.group(2)

                            characteristics = re.findall(r"([\w\s-]+) <([\w\s-]+)>", traits_info)

                            for characteristic, trait_category in characteristics:
                                if trait_category not in fieldnames:
                                    fieldnames.append(trait_category)

                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                            if csvfile.tell() == 0:
                                writer.writeheader()

                            row_data = {'Species': species_name}

                            for characteristic, trait_category in characteristics:
                                row_data[trait_category] = characteristic

                            writer.writerow(row_data)
