from argparse import ArgumentParser
import re

import pandas as pd

# Mapping of textual numbers to numeric
number_mapping = {
    "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8,
    "nine": 9, "ten": 10
}


def replace_textual_numbers(s):
    for text_num, num in number_mapping.items():
        s = s.replace(text_num, str(num))
    return s


def extract_numbers(s):
    numbers = []
    for match in re.finditer(r'(\d+\.?\d*)\s*-\s*(\d+\.?\d*)|\d+\.?\d*', s):
        if match.group(1) and match.group(2):
            numbers.extend([float(match.group(1)), float(match.group(2))])
        else:
            numbers.append(float(match.group(0)))
    return numbers


def find_min_max_or_concatenate(df):
    results = []
    for col in df.columns:
        all_numbers = []
        all_strings = []
        contains_mm = False
        for value in df[col].dropna():
            if 'mm' in str(value).lower():
                contains_mm = True
            numbers = extract_numbers(str(value))
            if numbers:
                all_numbers.extend(numbers)
            else:
                all_strings.append(str(value))
        if all_numbers:
            col_min = min(all_numbers)
            col_max = max(all_numbers)
            range_str = f"{col_min} - {col_max}" + (" mm" if contains_mm else "")
            results.append([col, range_str])
        elif all_strings:
            concatenated = "; ".join(all_strings) + (" mm" if contains_mm else "")
            results.append([col, concatenated])
        else:
            results.append([col, "N/A"])
    return pd.DataFrame(results, columns=["trait", "value or range"])


def combine_synonymous_columns(df, synonym_groups):
    for synonyms in synonym_groups:
        primary_col = synonyms[0]  # The first synonym will be the column name
        # Create a combined column if it doesn't already exist
        if primary_col not in df.columns:
            df[primary_col] = pd.NA

        # Iterate over each synonym to combine data
        for col in synonyms[1:]:  # Skip the first synonym since it's the primary column
            if col in df.columns:
                # Combine current data with the primary column, prioritizing non-NA values
                df[primary_col] = df[primary_col].combine_first(df[col])
                # Drop the synonym column after combining its data
                df.drop(columns=[col], inplace=True)
    return df


def main():
    parser = ArgumentParser(description="Filter traits for a specific reptile family")
    parser.add_argument("family", type=str, help="Reptile family to filter")
    args = parser.parse_args()

    family = args.family
    family = family.lower()
    file_path = f'.\\data\\LLaMA2 Results\\{family.title()}\\traits_{family}.csv'

    # Family-specific traits that Peter specifically wants
    traits = {
        "viperidae": [
            ["species"],
            ["ventral scales", "ventral scale counts", "ventral", "ventrals", "ventral scale", "VS", "VSC", "VEN", "V"],
            ["subcaudal scales", "subcaudal scale", "subcaudal[s]", "subcaudal", "subcaudals", "sub-caudal",
             "sub-caudals", "caudal", "caudals", "urostege", "urosteges", "SC", "C"],
            ["dorsal scale rows", "dorsal scale row", "dorsals", "dorsal", "DSR", "dorsal scale formula",
             "dorsal scale rows behind head", "dorsal scale rows behind midbody", "dorsal scale rows before tail",
             "anterior dorsal scale rows", "posterior dorsal scale rows", "anterior/posterior dorsal scale rows",
             "middorsal scale count"],
            ["scale", "scale type", "scales"],
            ["size", "total length", "length", "TL", "measurements"],
            ["SVL", "snout-vent length", "snout-vent-length", "snout vent length"],
            ["tail", "tails", "tail length", "TL", "TAL"],
            ["anal plate", "anal plates"],
            ["supralabial", "supralabials", "SL"],
            ["infralabial", "infralabials", "lower labial", "lower labials", "sublabial", "sublabials"]
        ],
        "amphisbaenidae": [
            ["species"],
            ["anal shields", "anal shield", "precloacal shields"],
            ["autotomy", "caudal autotomy", "autotomy constriction", "autotomy level", "autotomy site"],
            ["caudal annuli", "tail annuli"],
            ["color", "color on the dorsal surface", "color pattern", "dorsal color", "dorsal pigmentation",
             "dorsum color"],
            ["dorsal sulci", "dorsal sulcus"],
            ["frontal shield", "frontal", "frontal shape"],
            ["infralabials", "lower labial"],
            ["preanal pores", "precloacal pores", "preclocals pores"],
            ["divisions of the annuli", "dorsal and ventral segments", "segments per midbody annulus",
             "dorsal plus ventral segments", "scales around midbody", "segments around midbody",
             "segments to a midbody annulus"],
            ["supralabial shield", "upper labial"]
        ]
    }

    df = pd.read_csv(file_path)
    specified_traits = traits.get(family, [])
    if not specified_traits:
        print(f"No specified traits found for {family}.")
        return

    df = combine_synonymous_columns(df, specified_traits)

    # Flatten the list of specified traits for filtering
    flattened_traits = [item for sublist in specified_traits for item in sublist]
    primary_columns = [group[0] for group in specified_traits]  # Extract primary column names

    # Update the filtering logic using primary column names
    filtered_columns = [col for col in df.columns if col in primary_columns]
    filtered_df = df[filtered_columns]

    # Save the filtered dataframe
    filtered_file_path = f'.\\data\\LLaMA2 Results\\{family.title()}\\filtered_traits_{family}.csv'
    filtered_df.to_csv(filtered_file_path, index=False)
    print(f"Filtered data with species saved to: {filtered_file_path}")

    # Load the filtered DataFrame to replace the textual numbers --> numerical
    df_filtered = pd.read_csv(filtered_file_path)

    # Replace textual numbers with actual numeric value
    for col in df_filtered.columns:
        df_filtered[col] = df_filtered[col].apply(
            lambda x: replace_textual_numbers(str(x)) if isinstance(x, str) else x)

    # Overwrite the same filtered CSV file with the replacements
    df_filtered.to_csv(filtered_file_path, index=False)
    print(f"Filtered data with numeric values updated in: {filtered_file_path}")

    df_numeric = pd.read_csv(filtered_file_path)

    # Find the min and max for each column or concatenate strings, and create a summary DataFrame
    summary_df = find_min_max_or_concatenate(df_numeric)
    summary_df = summary_df[summary_df['trait'] != 'species']

    # Adjusted writing of the summary to ensure proper trait names
    summary_file_path = f'.\\data\\LLaMA2 Results\\{family.title()}\\range_{family}.csv'
    summary_df.to_csv(summary_file_path, index=False)
    print(f"Summary with ranges or concatenated values saved to: {summary_file_path}")

    # Optionally, if you want to append the summary directly to the filtered file
    # Comment out the above two lines and use this block instead
    # with open(filtered_file_path, 'a') as f:
    #     f.write('\n\n')
    #     summary_df.to_csv(f, index=False, header=True)

if __name__ == "__main__":
    main()
