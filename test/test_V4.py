import pytest
from chains.LLaMA2.fewshot import TraitsExtractorV4
from prompts.LLaMA2.NER_prompt import prompt

@pytest.fixture
def traits_extractor():
    return TraitsExtractorV4()

def parse_output(text):
    entries = text.strip().split('\n')
    parsed_entries = []

    for entry in entries:
        parts = [part.strip() for part in entry.split('|')]
        name = parts[0].split('. ')[1]  # Remove the numbering
        description = parts[1]
        is_true = parts[2] == 'True'
        category = parts[3].rstrip('.')  # Remove the trailing period
        
        # Create a dictionary for the entry
        entry_dict = {
            'name': name,
            'description': description,
            'is_true': is_true,
            'category': category
        }
        
        parsed_entries.append(entry_dict)
    return parsed_entries

def assert_expected(dict, name, expected_is_true):
    for entry in dict:
        if entry["name"] == name:
            assert entry["is_true"] == expected_is_true, f"{name} is_true assertion failed"
            print(f"Assertion passed for {name}")
            return
    print(f"{name} not found")


def test_basic_traits(traits_extractor):
    diagnosis = """
    Amphisbaena leeseri  Sauria Amphisbaenidae Diagnosis: A small form of Amphisbaena with the postrostral head shields paired and without major fusions of head shields, with the midventral segments of each annulus as wide as long, and with a single pair of round precloacal pores (which is but faintly apparent in females). Specimens have 216 to 240 body annuli, 14 to 16 caudal annuli, an autotomy constriction at the fifth or sixth postcloacal annulus, 13 to 15 (normally 14) dorsal and 14 to 18 ventral segments to a midbody annulus, and 6 pre-cloacal segments. The color of each animal is dark brown dorsally, lighter ventrally, the color changing by a dropping out of pigmented segments. The posterior 15% of a segment is often light colored. The intersegmental raphes are light. (Gans 1964: 554) Detailed description: Gans 1964: 556.
    """
    result, _ = traits_extractor.run_with_retries(diagnosis, prompt)
    out_dict = parse_output(result)
    assert_expected(out_dict,"Amphisbaena leeseri",False)
    assert_expected(out_dict,"color",True)



# 1. Amphisbaena leeseri | no adjective | False | as this is a species name.
# 2. Sauria | no adjective | False | as this is an order.
# 3. Amphisbaenidae | no adjective | False | as this is a family.
# 4. postrostral head shields | paired | True | as this is a specific anatomical feature (anatomical feature).
# 5. midventral segments of each annulus | as wide as long | True | as it describes a particular segment of the body (anatomical feature).
# 6. precloacal pores | single pair, round | True | as this is a distinct anatomical structure (anatomical feature).
# 7. body annuli | 216-240 | True | as it refers to the number of body segments or rings (quantitative trait).
# 8. caudal annuli | 14-16 | True | as it refers to the number of caudal annuli (quantitative trait).
# 9. autotomy constriction | at the fifth or sixth postcloacal annulus | True | as this specifies a specific survival trait and its location on the body (anatomical feature).
# 10. dorsal segments | 13-15 | True | as it refers to the number of dorsal segments (quantitative trait).
# 11. ventral segments | 14-18 | True | as it refers to the number of ventral segments (quantitative trait).
# 12. pre-cloacal segments | 6 | True | as this refers to the number of pre-cloacal segments (quantitative trait).
# 13. Dorsal color | dark brown | True | as it is a color (color).
# 14. Ventral color | lighter | True | as it is a color (color).
# 15. posterior 15% of a segment | light colored | True | as it is a color (color).
# 16. intersegmental raphes | light | True | as it is a color (color).
