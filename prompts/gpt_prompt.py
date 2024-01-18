prompt = """
    Defn: An entity is an anatomical feature(anatomical feature), quantitative trait(quantitative trait), and physical characteristic(physical characteristic). An adjective is something that describes an entity, such as a number, range of numbers, shape, color, pattern, or other descriptor.
    Species, family, order, dates, times, persons, references, verbs, background information, non-specific descriptions, and background information are not entitites. Adjectives that describe another species that is not the original species mentioned at the start of the diagnosis is not an entity.
    
    Only output your knowledge. Do not ask questions or give other irrelevant information.
    
    Example 1: Amphisbaena leeseri  Sauria Amphisbaenidae Diagnosis: A small form of Amphisbaena with the postrostral head shields paired and without major fusions of head shields, with the midventral segments of each annulus as wide as long, and with a single pair of round precloacal pores (which is but faintly apparent in females). Specimens have 216 to 240 body annuli, 14 to 16 caudal annuli, an autotomy constriction at the fifth or sixth postcloacal annulus, 13 to 15 (normally 14) dorsal and 14 to 18 ventral segments to a midbody annulus, and 6 pre-cloacal segments. The color of each animal is dark brown dorsally, lighter ventrally, the color changing by a dropping out of pigmented segments. The posterior 15% of a segment is often light colored. The intersegmental raphes are light. (Gans 1964: 554) Detailed description: Gans 1964: 556.

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

    Example 2: Amphisbaena innocens Sauria Amphisbaenidae DESCRIPTION: Size large (SVL to 262 mm); tail to 18 mm, conical, rounded terminally; no caudal autotomy; body annuli 186-219, caudal annuli 10-15; dorsal segments 14-17/midbody annulus, ventral segments 18-22/midbody annulus; 3 rows of postgenials; no postmalar chin shields;  4-6 (strongly modally 4) precloacal pores; nasal suture rather long but less than one-half length of prefrontal suture; 1 temporal. Dorsum (as preserved) shades of brown, at times with dark violet head and tail, grading to chocolate brown on body; color solid on head and tail, on body rectangular centers of each segment much darker than margins, giving the impression of dark spots; color darker dorsally than ventrally but no white segments (Schwartz & Henderson 1991: 560). For a discussion of geographic variation see Gans & Alexander 1962: 101.

    1. Amphisbaena innocens | no adjective | False | as this is a species name.
    2. Sauria | no adjective | False | as this is an order.
    3. Amphisbaenidae | no adjective | False | as this is a family.
    4. Size | no adjective | False | as this refers to SVL = snout-vent-length
    5. SVL | 262 mm | True | as this is quantitative trait (quantitative trait)
    6. tail | 18 mm | True | as this is a quantitative trait (quantitative trait)
    7. Tail shape | conical, rounded terminally | True | as it is the shape of the tail (physical characteristic).
    8. caudal autotomy | no adjective | False | as it describes the lack of a feature.
    9. body annuli | 186-219 | True | as this describes the number of body annuli (quantitative trait).
    10. caudal annuli | 10-15 | True | as this is the number of caudal annuli (quantitative trait).
    11. dorsal segments/midbody annulus | 14-17 | True | as this is a quantitative trait (quantitative trait).
    12. ventral segments/midbody annulus | 18-22 | True | as this a quantitative trait (quantitative trait).
    13. rows of postgenials | 3  | True | as it is a physical characteristic(physical characteristic)
    14. postmalar chin shields | no adjective | True | as it is a physical characteristic(physical characteristic)
    15. precoacal pores | 4-6 | True | as it is a quantitative trait (quantitative trait).
    16. nasal suture | rather long | True | as it is an anatomical feature (anatomical feature).
    17. temporal | 1 | True | as it is a quantitative trait (quantitative trait).
    18. Dorsum color | shades of brown | True | as it is a color (color).
    19. head | dark violet | as it is a color (color).
    20. tail | dark violet | as it is a color (color).
    21. Body color | chocolate brown | True | as it is a color (color).
    22. color on head | solid | True | as it is a color (color).
    23. color on tail | solid | True | as it is a color (color).
    24. Dorsal color | darker dorsally than ventrally | True | as it is a color (color).
    25. white segments | no adjective | False | as it describes the lack of a feature.

    For this next example, follow the same format for your answer:
    """
