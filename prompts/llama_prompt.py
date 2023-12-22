prompt = """
    Defn: An entity is an anatomical feature(anatomical feature), quantitative trait(quantitative trait), physical characteristic(physical characteristic), distinctive trait(distinctive trait), and color description(color).
    Species, dates, times, persons, references, verbs, background information, non-specific descriptions, and background information are not entitites.

    Example 1: Amphisbaena leeseri	Sauria	Amphisbaenidae	Diagnosis: A small form of Amphisbaena with the 
    postrostral head shields paired and without major fusions of head shields, with the midventral segments of 
    each an nulus as wide as long, and with a single pair of round precloacal pores (which is but faintly 
    apparent in females). Specimens have 216 to 240 body annuli, 14 to 16 caudal annuli, an autotomy 
    constriction at the fifth or sixth postcloacal annulus, 13 to 15 (normally 14) dorsal and 14 to 18 ventral 
    segments to a midbody annulus, and 6 pre-cloacal segments. The color of each animal is dark brown 
    dorsally, lighter ventrally, the color changing by a dropping out of pigmented segments. The posterior 15% 
    of a segment is often light colored. The intersegmental raphes are light. (Gans 1964: 554) Detailed 
    description: Gans 1964: 556."
    
    Answer:
    1. Amphisbaena leeseri | False | as this is a species name.
    2. Sauria | False | as this is an order.
    3. postostral head shields | True | as this is a specific anatomical feature (anatomical feature).
    4. midventral segments | True | as it describes a particular segment of the body (anatomical feature).
    5. single pair of round precloacal pores | True | as this is a distinct anatomical structure (anatomical feature).
    6. 216 to 240 body annuli | True | as it refers to the number of body segments or rings (quantitative trait).
    7. 14 to 16 caudal annuli | True | as it refers to the number of caudal annuli (quantitative trait).
    8. autotomy constriction | True | as this specifies a specific survival trait and its location on the body (anatomical feature).
    9. 13 to 15 dorsal segments | True | as it refers to the number of dorsal segments (quantitative trait).
    10. 14 to 18 ventral segments | True | as it refers to the number of ventral segments (quantitative trait).
    11. 6 pre-cloacal segments | True | as this refers to the number of pre-cloacal segments (quantitative trait).
    12. dark brown dorsally | True | as it is a color (color).
    13. lighter ventrally | True | as it is a color (color).
    14. posterior 15% | False | as it is not a specific trait.
    15. light intersegmental raphes | True | as it is a color (color).

    Example 2: Amphisbaena innocens	Sauria	Amphisbaenidae	DESCRIPTION: Size large (SVL to 262 mm); tail to 18 mm, 
    conical, rounded terminally; no caudal autotomy; body annuli 186-219, caudal annuli 10-15; dorsal segments 
    14-17/midbody annulus, ventral segments 18-22/midbody annulus; 3 rows of postgenials; no postmalar chin shields; 
    4-6 (strongly modally 4) precloacal pores; nasal suture rather long but less than one-half length of prefrontal 
    suture; 1 temporal. Dorsum (as preserved) shades of brown, at times with dark violet head and tail, grading to 
    chocolate brown on body; color solid on head and tail, on body rectangular centers of each segment much darker 
    than margins, giving the impression of dark spots; color darker dorsally than ventrally but no white segments 
    (Schwartz & Henderson 1991: 560).For a discussion of geographic variation see Gans & Alexander 1962: 101.
    
    Answer:
    1. Amphisbaena innocents | False | as this is a species name.
    2. Sauria | False | as this is an order.
    3. Size | False | as this is a non-specific description.
    4. SVL to 262 mm | True | as this is quantitative trait (quantitative trait).
    5. tail to 18 mm | True | as this is a quantitative trait (quantitative trait).
    6. tail conical, rounded terminally | True | as this describes the shape of the tail (physical characteristic).
    7. no caudal autotomy | True | as it describes the lack of a feature (distinctive trait).
    8. 186-219 body annuli | True | as this describes the number of body annuli (quantitative trait).
    9. 10-15 caudal annuli | True | as this is the number of caudal annuli (quantitative trait).
    10. 14-17 dorsal segments/midbody annulus | True | as this is a quantitative trait (quantitative trait).
    11. 18-22 ventral segments/midbody annulus | True | as this a quantitative trait (quantitative trait).
    12. 3 rows of postgenials | True | as it is a distinctive trait (distinctive trait).
    13. no postmalar chin shields | True | as it is a distinctive trait (distinctive trait).
    14. 4-6 precoacal pores | True | as it is a quantitative trait (quantitative trait).
    15. nasal suture rather long | True | as it is an anatomical feature (anatomical feature).
    16. 1 temporal | True | as it is a quantitative trait (quantitative trait).
    17. Dorsum shades of brown | True | as it is a color (color).
    18. dark violet head and tail | True | as it is a color (color).
    19. chocolate brown on body | True | as it is a color (color).
    20. color solid on head and tail | True | as it is a color (color).
    21. color darker dorsally than ventrally | True | as it is a color (color).
    22. no white segments | True | as it describes the lack of a feature (distinctive trait).
    
    For this next example, only output your answer in the same format as the answers above and nothing else:
    """
