import io
import os
import csv
import re
import streamlit as st
from dotenv import load_dotenv
import argparse
import pandas as pd
import streamlit_ext as ste
from zero_shot import TraitsExtractor
from zero_shot_v2 import TraitsExtractorV2

def process_uploaded_file(uploaded_file, traits_extractor):
    trait_categories = set()
    species_data = []

    if isinstance(uploaded_file, str):
        # Command line execution, open the file normally
        file_to_read = open(uploaded_file, 'r', encoding='utf-8')
    else:
        # Streamlit execution, use the file-like object
        bytes_data = uploaded_file.getvalue()
        file_to_read = io.TextIOWrapper(io.BytesIO(bytes_data), encoding='utf-8')

    with file_to_read as file:
        for line in file:
            input_line = line.split()
            species = ' '.join(input_line[0:2])
            diagnosis = ' '.join(input_line[2:])

            if species:
                categorized_traits = traits_extractor.get_categorized_traits().run(f"{species}: {diagnosis}")
                match = re.match(r"([\w\s-]+): (.+)", categorized_traits)

                if match:
                    species_name = species
                    traits_info = match.group(2)

                    characteristics = re.findall(r"([\w\s-]+) <([\w\s-]+)>", traits_info)

                    for _, trait_category in characteristics:
                        trait_categories.add(trait_category)

                    species_data.append({'Species': species_name, 'Characteristics': characteristics})

    return species_data, trait_categories


def write_to_csv(species_data, trait_categories, filename):
    fieldnames = ['Species'] + list(trait_categories)
    data_list = []

    for data in species_data:
        row_data = {'Species': data['Species']}
        for characteristic, trait_category in data['Characteristics']:
            row_data[trait_category] = characteristic
        data_list.append(row_data)

    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)
    
    return pd.DataFrame(data_list)


def main(file_path=None, version=None):
    load_dotenv()
    API_KEY = os.environ['OPENAI_API_KEY']

    traits_extractor_v1 = TraitsExtractor()
    traits_extractor_v2 = TraitsExtractorV2()

    # Determine the execution context
    if file_path and version:
        # Command Line Execution
        if version == 1:
            traits_extractor = traits_extractor_v1
            output_filename = 'extracted_traits_v1.csv'
        elif version == 2:
            traits_extractor = traits_extractor_v2
            output_filename = 'extracted_traits_v2.csv'
        else:
            raise ValueError("Invalid version specified. Choose 1 or 2.")

        species_data, trait_categories = process_uploaded_file(file_path, traits_extractor)
        df = write_to_csv(species_data, trait_categories, output_filename)
        df.to_csv(output_filename, index=False, encoding='utf-8')
        print(f"Output saved to {output_filename}")
    else:
        # Streamlit UI Execution
        import streamlit as st
        import streamlit_ext as ste

        st.set_page_config(page_title="ReptileLLM", layout="wide")
        st.title("🦎 ReptileLLM")

        version1_tab, version2_tab = st.tabs(["Version 1", "Version 2"])

    with version1_tab:
        uploaded_file_v1 = st.file_uploader("Upload your data", key="v1")
        species_data_v1, trait_categories_v1 = process_uploaded_file(uploaded_file_v1, traits_extractor_v1)
        df_v1 = write_to_csv(species_data_v1, trait_categories_v1, 'extracted_traits_v1.csv')
        csv_v1 = df_v1.to_csv(index=False, encoding='utf-8')
        ste.download_button("Download data as CSV", csv_v1, "traits_v1.csv")

    with version2_tab:
        uploaded_file_v2 = st.file_uploader("Upload your data", key="v2")
        species_data_v2, trait_categories_v2 = process_uploaded_file(uploaded_file_v2, traits_extractor_v2)
        df_v2 = write_to_csv(species_data_v2, trait_categories_v2, 'extracted_traits_v2.csv')
        csv_v2 = df_v2.to_csv(index=False, encoding='utf-8')
        ste.download_button("Download data as CSV", csv_v2, "traits_v2.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process reptile species data.")
    parser.add_argument('file', type=str, help='Path to the input file')
    parser.add_argument('version', type=int, help='Version of the Traits Extractor (1 or 2)')
    args = parser.parse_args()
    main(args.file, args.version)