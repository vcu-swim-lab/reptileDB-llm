import io
import os
import csv
import re
import streamlit as st
from dotenv import load_dotenv
from zero_shot import TraitsExtractor
from zero_shot_v2 import TraitsExtractorV2
import pandas as pd
from awesome_table import AwesomeTable
import streamlit_ext as ste

traits = TraitsExtractor()
traits_v2 = TraitsExtractorV2()

load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

if __name__ == "__main__":
    st.set_page_config(page_title="ReptileLLM", layout="wide")
    st.title("🦎 ReptileLLM")

    version1_tab, version2_tab = st.tabs(["Version 1", "Version 2"])
    with version1_tab:
        uploaded_file = st.file_uploader("Upload your data", key="v1")

        trait_categories = set()
        species_data = []
        data_list = []

        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            with io.TextIOWrapper(io.BytesIO(bytes_data), encoding='utf-8') as file:
                for line in file:
                    input_line = line.split()
                    species = ' '.join(input_line[0:2])
                    diagnosis = ' '.join(input_line[2:])

                    if species:
                        categorized_traits = traits.get_categorized_traits().run(f"{species}: {diagnosis}")
                        match = re.match(r"([\w\s-]+): (.+)", categorized_traits)

                        if match:
                            species_name = species
                            traits_info = match.group(2)

                            characteristics = re.findall(r"([\w\s-]+) <([\w\s-]+)>", traits_info)

                            for _, trait_category in characteristics:
                                trait_categories.add(trait_category)

                            species_data.append({'Species': species_name, 'Characteristics': characteristics})

            with open('extracted_traits.csv', mode='w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Species'] + list(trait_categories)
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()

                for data in species_data:
                    row_data = {'Species': data['Species'],
                                }
                    for characteristic, trait_category in data['Characteristics']:
                        row_data[trait_category] = characteristic

                    data_list.append(row_data)

            table = AwesomeTable(pd.json_normalize(data_list), show_order=True)

            df = pd.DataFrame(data_list)
            csv = df.to_csv(index=False, encoding='utf-8')
            ste.download_button("Download data as CSV", csv, "traits.csv")

        with version2_tab:
            uploaded_file2 = st.file_uploader("Upload your data", key="v2")

            trait_categories2 = set()
            species_data2 = []
            data_list2 = []

            if uploaded_file2 is not None:
                bytes_data = uploaded_file2.getvalue()
                with io.TextIOWrapper(io.BytesIO(bytes_data), encoding='utf-8') as file:
                    for line in file:
                        input_line = line.split()
                        species = ' '.join(input_line[0:2])
                        diagnosis = ' '.join(input_line[2:])

                        if species:
                            categorized_traits = traits_v2.get_categorized_traits().run(f"{species}: {diagnosis}")
                            match = re.match(r"([\w\s-]+): (.+)", categorized_traits)

                            if match:
                                species_name = species
                                traits_info = match.group(2)

                                characteristics = re.findall(r"([\w\s-]+) <([\w\s-]+)>", traits_info)

                                for _, trait_category in characteristics:
                                    trait_categories2.add(trait_category)

                                species_data2.append({'Species': species_name, 'Characteristics': characteristics})

                with open('extracted_traits.csv', mode='w', newline='', encoding='utf-8') as csvfile2:
                    fieldnames = ['Species'] + list(trait_categories2)
                    writer2 = csv.DictWriter(csvfile2, fieldnames=fieldnames)

                    writer2.writeheader()

                    for data in species_data2:
                        row_data = {'Species': data['Species'],
                                    }
                        for characteristic, trait_category in data['Characteristics']:
                            row_data[trait_category] = characteristic

                        data_list2.append(row_data)

                table = AwesomeTable(pd.json_normalize(data_list2), show_order=True)

                df = pd.DataFrame(data_list2)
                csv_data = df.to_csv(index=False, encoding='utf-8')
                ste.download_button("Download data as CSV", csv_data, "traits.csv")
