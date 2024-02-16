import re
import pandas as pd

def color_substring(description, substring, color):
    pattern = r'(?<!\w)(?:[.,;!?]?\s?)' + re.escape(substring) + r'(?:\s?[.,;!?]?)(?!\w)'
    replacement = f' <span style="color: {color};">{substring}</span> '
    colored_description = re.sub(pattern, replacement, description, flags=re.IGNORECASE)
    return colored_description

def generate_html_content(family_name):
    df = pd.read_csv(f"traits_{family_name}.csv")

    output_html_content = "<html><body>\n"

    with open(f'data/{family_name}.txt', 'r', encoding='utf-8') as file:
        for line in file:
            modified_line = line.strip().replace(';', '|')
            missed_attributes = []

            for _, row in df.iterrows():
                species_name = row['species']
                if re.search(re.escape(species_name), modified_line, re.IGNORECASE):
                    for trait in df.columns[1:]:
                        if pd.notna(row[trait]):
                            trait_found = re.search(re.escape(trait), modified_line, re.IGNORECASE)
                            attribute_found = re.search(re.escape(str(row[trait])), modified_line, re.IGNORECASE)
                            if trait_found or attribute_found:
                                modified_line = color_substring(modified_line, trait, "red")
                                modified_line = color_substring(modified_line, str(row[trait]), "green")
                            elif not trait_found:
                                missed_attributes.append(f"{trait}: {row[trait]}")

            output_html_content += f"{modified_line}<br>\n"

            for attribute in missed_attributes:
                output_html_content += f"<i>{attribute}</i><br>\n"
            output_html_content += "<br>\n" 

    output_html_content += "</body></html>\n"

    with open(f'debug_{family_name}.html', 'w', encoding='utf-8') as html_file:
        html_file.write(output_html_content)