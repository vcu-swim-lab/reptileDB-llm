import re
import pandas as pd
from argparse import ArgumentParser

def color_substring(description, substring, color):
    pattern = re.compile(r'(?<!\w)(?:\s?[.,;!?]?)' + re.escape(substring) + r'(?:\s?[.,;!?]?)(?<!\w)', re.IGNORECASE) ##Might be the problem
    replacement = f' <span style="color: {color};">{substring}</span> '
    colored_description = re.sub(pattern, replacement, description)
    return colored_description

def generate_html_content(in_file, traits_file):
    df = pd.read_csv(traits_file)

    output_html_content = "<html><body>\n"

    with open(in_file, 'r', encoding='utf-8') as file:
        for line in file:
            modified_line = line.strip().replace(';', ' | ')
            if modified_line.__contains__('') or modified_line.__contains__(''):
                remodified_line = modified_line.replace('', ' ').replace('', ' ')
                missed_attributes = []
            
            for _, row in df.iterrows(): ##ignoring index value while iterating
                species_name = row['species'] ##each row with each species name is recorded inside species_name
                if re.search(re.escape(species_name), remodified_line, re.IGNORECASE): ##ignoring special characters in species_name, search inside each remodified_line from file
                    for trait in df.columns[1:]: ##for each column, (naming it trait) and ignoring column 0 cus its all species_names
                        if pd.notna(row[trait]): #if values in the trait column are not missing, proceed
                            trait_found = re.search(re.escape(trait), remodified_line, re.IGNORECASE)
                            attribute_found = re.search(re.escape(str(row[trait])), remodified_line, re.IGNORECASE)
                            if trait_found or attribute_found:
                                remodified_line = color_substring(remodified_line, trait, "red")
                                remodified_line = color_substring(remodified_line, str(row[trait]), "green")
            output_html_content += f"{remodified_line}<br>\n"

            with open(f'debug_out.html', 'w', encoding='utf-8') as html_file:
                html_file.write(output_html_content)  # Writing HTML content without escaping

if __name__ == "__main__":
    parser = ArgumentParser(description="Debugging script.")
    parser.add_argument('file', type=str, help='Path to the input file')
    parser.add_argument('traits_file', type=str, help='Path to the LLM output file')
    args = parser.parse_args()
    generate_html_content(args.file, args.traits_file)