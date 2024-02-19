import csv
import re
import pandas as pd

def process_line(line, traits_extractor, version):
    """Process a single line of species data."""
    if not line.strip():
        return None, None

    family, species_info = extract_species_info(line, traits_extractor, version)
    species, diagnosis, characteristics = species_info

    if species and diagnosis:
        if isinstance(characteristics, str):
            characteristics = [(characteristics, '')]

        return {'Species': species, 'Family': family, 'Characteristics' if version in [1, 2] else 'Categories':
            characteristics}, set(trait for _, trait in characteristics)

    return None, None


def count_categories_for_family(species_data, family_name):
    """Count the amount of times a term appears for a given family."""
    category_counts = {}
    for species_dict in species_data:
        if species_dict['Family'] == family_name:
            categories = species_dict['Categories']
            for category_tuple in categories:
                category_list = category_tuple[0].split(', ')
                for category in category_list:
                    if category:
                        category_counts[category] = category_counts.get(category, 0) + 1

    return category_counts


def write_term_counts_to_csv(family_name, category_counts, filename):
    """Write term counts to a csv file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Family', 'Category', 'Count'])
        for category, count in category_counts.items():
            writer.writerow([family_name, category, count])


def process_species_data(file, traits_extractor, version):
    """Adds species data to a dictionary and set for further processing."""
    trait_categories = set()
    species_data = []

    with file as file_stream:
        for line in file_stream:
            data, traits = process_line(line, traits_extractor, version)
            if data:
                trait_categories.update(trait for trait in traits if trait != 'Diagnosis')
                species_data.append(data)

    return species_data, trait_categories


def extract_species_info(line, traits_extractor, version):
    """Extracts specific words from species data."""
    elements = line.split()
    genus = elements[0]
    epithet = elements[1]
    species = genus + " " + epithet
    order = elements[2]
    family = elements[3]
    abstract = ' '.join(elements[4:])

    categorized_traits = traits_extractor.get_categorized_traits().run(f"{species}: {abstract}")
    if version == 3:
        return family, parse_categories_v3(species, abstract, categorized_traits)
    else:
        return family, parse_characteristics_v1v2(species, abstract, categorized_traits)


def parse_characteristics_v1v2(species, abstract, categorized_traits):
    """Extracts characteristics from species data."""
    match = re.match(r"([\w\s-]+): (.+)", categorized_traits)
    if match:
        characteristics = re.findall(r"([\w\s-]+) <([\w\s-]+)>", match.group(2))
        return species, abstract, characteristics
    return species, abstract, []


def parse_categories_v3(species, abstract, categorized_traits):
    """Extracts categories from species data."""
    categories_split = categorized_traits.split()
    categories_list = categories_split[1:]
    categories = ' '.join(categories_list)
    return species, abstract, categories


def write_to_csv(species_data, trait_categories, filename, version):
    """Writes species names, their categories, and their descriptions to a csv file."""
    fieldnames = ['Species'] + sorted(trait_categories)
    rows = [create_csv_row(data, version) for data in species_data]

    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return pd.DataFrame(rows)


def create_csv_row(data, version):
    """Helper method for write_to_csv that creates a csv row."""
    char_or_cat = 'Characteristics' if version in [1, 2] else 'Categories'
    row = {'Species': data['Species']}
    for characteristic, trait in data[char_or_cat]:
        row[trait] = characteristic
    return row
