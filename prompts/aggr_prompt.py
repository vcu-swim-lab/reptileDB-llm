prompt = """
    [INST]
    Defn: An entity is an anatomical feature(anatomical feature), quantitative trait(quantitative trait), and physical characteristic(physical characteristic). An adjective is something that describes an entity, such as a number, range of numbers, shape, color, pattern, a combination of any of those, or other descriptor.
    Species, family, order, dates, times, persons, references, verbs, background information, non-specific descriptions, and background information are not entitites.
    [/INST]

    <s>[INST]
    Example 1: Amphisbaena leeseri  Sauria Amphisbaenidae Diagnosis: A small form of Amphisbaena with the postrostral head shields paired and without major fusions of head shields, with the midventral segments of each annulus as wide as long, and with a single pair of round precloacal pores (which is but faintly apparent in females). Specimens have 216 to 240 body annuli, 14 to 16 caudal annuli, an autotomy constriction at the fifth or sixth postcloacal annulus, 13 to 15 (normally 14) dorsal and 14 to 18 ventral segments to a midbody annulus, and 6 pre-cloacal segments. The color of each animal is dark brown dorsally, lighter ventrally, the color changing by a dropping out of pigmented segments. The posterior 15% of a segment is often light colored. The intersegmental raphes are light. (Gans 1964: 554) Detailed description: Gans 1964: 556.
    [/INST]

    Answer:
    1. Amphisbaena leeseri | no adjective | False | as this is a species name.
    2. Sauria | no adjective | False | as this is an order.
    3. Amphisbaenidae | no adjective | False | as this is a family.
    </s>

    [INST]
    Example 2: Amphisbaena innocens Sauria Amphisbaenidae DESCRIPTION: Size large (SVL to 262 mm); tail to 18 mm, conical, rounded terminally; no caudal autotomy; body annuli 186-219, caudal annuli 10-15; dorsal segments 14-17/midbody annulus, ventral segments 18-22/midbody annulus; 3 rows of postgenials; no postmalar chin shields;  4-6 (strongly modally 4) precloacal pores; nasal suture rather long but less than one-half length of prefrontal suture; 1 temporal. Dorsum (as preserved) shades of brown, at times with dark violet head and tail, grading to chocolate brown on body; color solid on head and tail, on body rectangular centers of each segment much darker than margins, giving the impression of dark spots; color darker dorsally than ventrally but no white segments (Schwartz & Henderson 1991: 560). For a discussion of geographic variation see Gans & Alexander 1962: 101.
    [/INST]

    <s>
    Answer:
    1. Amphisbaena innocens | no adjective | False | as this is a species name.
    2. Sauria | no adjective | False | as this is an order.
    3. Amphisbaenidae | no adjective | False | as this is a family.
    </s>

    [INST]For this next example, follow the same format for your answer:
    """
