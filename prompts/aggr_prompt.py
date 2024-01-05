prompt = """
    [INST]
    Defn: An entity is an anatomical feature(anatomical feature), quantitative trait(quantitative trait), and physical characteristic(physical characteristic). An adjective is something that describes an entity, such as a number, range of numbers, shape, color, pattern, a combination of any of those, or other descriptor.
    Species, family, order, dates, times, persons, references, verbs, background information, non-specific descriptions, and background information are not entitites.

    <s>
    Example 1: Amphisbaena leeseri  Sauria Amphisbaenidae Diagnosis: A small form of Amphisbaena with the postrostral head shields paired and without major fusions of head shields, with the midventral segments of each annulus as wide as long, and with a single pair of round precloacal pores (which is but faintly apparent in females). Specimens have 216 to 240 body annuli, 14 to 16 caudal annuli, an autotomy constriction at the fifth or sixth postcloacal annulus, 13 to 15 (normally 14) dorsal and 14 to 18 ventral segments to a midbody annulus, and 6 pre-cloacal segments. The color of each animal is dark brown dorsally, lighter ventrally, the color changing by a dropping out of pigmented segments. The posterior 15% of a segment is often light colored. The intersegmental raphes are light. (Gans 1964: 554) Detailed description: Gans 1964: 556.

    Answer:
    1. Amphisbaena leeseri | no adjective | False | This is a species name.
    2. Sauria | no adjective | False | Classified as an order.
    3. Amphisbaenidae | no adjective | False | Identified as a family.
    4. Paired postrostral head shields | True | Describes a specific anatomical feature.
    5. Midventral segments of each annulus | True | Refers to a particular body segment (anatomical feature).
    6. Single round precloacal pore | True | Represents a distinct anatomical structure.
    7. Body annuli | 216 to 240 | True | Indicates the number of body segments (quantitative trait).
    8. Caudal annuli | 14 to 16 | True | Indicates the quantity of caudal annuli (quantitative trait).
    9. Autotomy constriction | at the fifth or sixth postcloacal annulus | True | Specifies a survival trait and its location on the body (anatomical feature).
    10. Dorsal segments | 13 to 15 | True | Refers to the number of dorsal segments (quantitative trait).
    11. Ventral segments | 14 to 18 | True | Indicates the number of ventral segments (quantitative trait).
    12. Pre-cloacal segments | 6 | True | Represents the number of pre-cloacal segments (quantitative trait).
    13. Dorsal color | dark brown | True | Denotes the color (color).
    14. Ventral color | lighter | True | Specifies the color (color).
    15. The rear 15% of a segment | light colored | True | Represents the coloration (color).
    16. intersegmental raphes | light | True | Refers to the coloration (color).
    [/INST]</s>

    For this next example, follow the same format for your answer:
    """
