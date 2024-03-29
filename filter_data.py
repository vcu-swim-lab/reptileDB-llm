from argparse import ArgumentParser
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


if __name__ == "__main__":
    main()
