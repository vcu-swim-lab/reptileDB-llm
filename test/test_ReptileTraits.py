import pytest
from reptile_traits import ReptileTraits

@pytest.fixture
def peter_annotated_output():
    return """
    1. Amphisbaena leeseri | no adjective | False | as this is a species name.
    2. Sauria | no adjective | False | as this is an order.
    3. Amphisbaenidae | no adjective | False | as this is a family.
    4. postrostral head shields | paired | True | as this is a specific anatomical feature (anatomical feature).
    5. midventral segments of each annulus | as wide as long | True | as it describes a particular segment of the body (anatomical feature).
    6. precloacal pores | single pair, round | True | as this is a distinct anatomical structure (anatomical feature).
    7. body annuli | 216-240 | True | as it refers to the number of body segments or rings (quantitative trait).
    8. caudal annuli | 14-16 | True | as it refers to the number of caudal annuli (quantitative trait).
    9. autotomy constriction | at the fifth or sixth postcloacal annulus | True | as this specifies a specific survival trait and its location on the body (anatomical feature).
    10. dorsal segments | 13-15 | True | as it refers to the number of dorsal segments (quantitative trait).
    11. ventral segments | 14-18 | True | as it refers to the number of ventral segments (quantitative trait).
    12. pre-cloacal segments | 6 | True | as this refers to the number of pre-cloacal segments (quantitative trait).
    13. Dorsal color | dark brown | True | as it is a color (color).
    14. Ventral color | lighter | True | as it is a color (color).
    15. posterior 15% of a segment | light colored | True | as it is a color (color).
    16. intersegmental raphes | light | True | as it is a color (color).
    """

def test_output_parser_basic():
    output_text = []
    result = """
    Size | Not Applicable | False | refers to SVL.
    SVL | 198-248 mm | True | quantitative.
    """
    output_text.append(("species_name", result))
    csv_out = ReptileTraits.parse_output_text(output_text)
    expected_output = {'species_name': {'svl': '198-248 mm'}}
    assert csv_out == expected_output

def test_output_peter(peter_annotated_output):
    output_text = []
    output_text.append(("species_name", peter_annotated_output))
    csv_out = ReptileTraits.parse_output_text(output_text)
    assert 'Amphisbaenidae' not in csv_out['species_name'].keys()
    assert csv_out['species_name']['postrostral head shields'] == 'paired'
    assert csv_out['species_name']['dorsal color'] == 'dark brown'


@pytest.mark.skip(reason="this ability not implemeted at the moment")
def test_one_less_column():
    output_text = []
    result = """
    SVL | 198-248 mm | True
    """
    output_text.append(("species_name", result))
    csv_out = ReptileTraits.parse_output_text(output_text)
    expected_output = {'species_name': {'svl': '198-248 mm'}}
    assert csv_out == expected_output
    pass
