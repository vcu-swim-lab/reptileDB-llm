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
    # Replace textual numbers with their numerical value, good for parsing later
    for text_num, num in number_mapping.items():
        s = s.replace(text_num, str(num))
    return s


def extract_numbers(s):
    """
    Extracts all numbers from the input string and returns them as a list of floats.
    This function handles ranges by considering only the endpoints.
    """
    numbers = []
    # Match all patterns resembling numbers or ranges of numbers
    for match in re.finditer(r'(\d+\.?\d*)\s*-\s*(\d+\.?\d*)|\d+\.?\d*', s):
        if match.group(1) and match.group(2):  # If it's a range, add both ends
            numbers.extend([float(match.group(1)), float(match.group(2))])
        else:  # Otherwise, just add the number
            numbers.append(float(match.group(0)))
    return numbers


def find_min_max_or_concatenate(df):
    """
    Finds the minimum and maximum numbers in each column of the DataFrame, or concatenates all strings
    if no numbers are found. Returns a DataFrame with the 'trait' and its 'range' or concatenated string as columns.
    """
    results = []
    for col in df.columns:
        all_numbers = []
        all_strings = []
        for value in df[col].dropna():
            numbers = extract_numbers(str(value))
            if numbers:
                all_numbers.extend(numbers)
            else:
                all_strings.append(str(value))
        if all_numbers:  # If there are numbers, find min and max
            col_min = min(all_numbers)
            col_max = max(all_numbers)
            results.append([col, f"{col_min}-{col_max}"])
        elif all_strings:  # If no numbers but there are strings, concatenate them
            concatenated = ", ".join(all_strings)  # Change the separator if needed
            results.append([col, concatenated])
        else:
            results.append([col, "N/A"])
    return pd.DataFrame(results, columns=["trait", "value or range"])


def main():
    parser = ArgumentParser(description="Filter traits for a specific reptile family")
    parser.add_argument("family", type=str, help="Reptile family to filter")
    args = parser.parse_args()

    family = args.family
    family = family.lower()
    file_path = f'.\\data\\LLaMA2 Results\\{family.title()}\\traits_{family}.csv'

    # Family-specific traits that Peter specifically wants
    traits = {
        "amphisbaenidae": [
            "species",
            "ventral scale counts", "ventral", "ventrals", "ventral scale", "ventral scales", "VS", "VSC", "VEN", "V",
            "subcaudal scales", "subcaudal scale", "subcaudal[s]", "subcaudal", "subcaudals", "sub-caudal",
            "sub-caudals", "caudal", "caudals", "urostege", "urosteges", "SC", "C",
            "dorsal scale rows", "dorsal scale row", "dorsals", "dorsal", "DSR", "dorsal scale formula",
            "dorsal scale rows behind head", "dorsal scale rows behind midbody", "dorsal scale rows before tail",
            "anterior dorsal scale rows", "posterior dorsal scale rows", "anterior/posterior dorsal scale rows",
            "middorsal scale count",
            "scale", "scale type", "scales",
            "size", "total length", "length", "TL", "measurements",
            "SVL", "snout-vent length", "snout-vent-length", "snout vent length",
            "tail", "tails", "tail length", "TL", "TAL",
            "anal plate", "anal plates",
            "supralabial", "supralabials", "SL",
            "infralabial", "infralabials", "lower labial", "lower labials", "sublabial", "sublabials"
        ],
        "viperidae": [
            "species",
            "anal shields", "precloacals shields",
            "autotomy", "caudal autotomy", "autotomy constriction", "autotomy level", "autotomy site",
            "caudal annuli", "tail annuli",
            "color", "color on the dorsal surface", "color pattern", "dorsal color", "dorsal pigmentation",
            "dorsum color",
            "dorsal sulci", "dorsal sulcus",
            "frontal", "frontal shield", "frontal shape",
            "infralabials", "lower labial",
            "preanal pores", "precloacal pores", "preclocals pores",
            "divisions of the annuli", "dorsal and ventral segments", "segments per midbody annulus",
            "dorsal plus ventral segments", "scales around midbody", "segments around midbody",
            "segments to a midbody annulus",
            "supralabial shield", "upper labial"
        ]
    }

    specified_traits = traits.get(family, [])
    if not specified_traits:
        print(f"No specified traits found for {family}.")
        return

    # Load the dataframe
    df = pd.read_csv(file_path)

    # Filter the DataFrame for specified traits, ignoring case
    filtered_columns = [col for col in df.columns if col.lower() in map(str.lower, specified_traits)]
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

    # Write the summary to the file, skipping two rows at the beginning
    with open(filtered_file_path, 'a') as f:
        f.write('\n\n')

        # Write the header
        f.write("Trait,Range\n")

        # Write each row of the summary DataFrame, skipping one row after each
        for index, row in summary_df.iterrows():
            if row['trait'] != "species":
                line = f"{row['trait']},{row['value or range']}\n"
                f.write(line)

    print(f"Summary with ranges or concatenated values added to: {filtered_file_path}")


if __name__ == "__main__":
    main()
