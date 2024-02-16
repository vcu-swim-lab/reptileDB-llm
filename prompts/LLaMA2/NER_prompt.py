prompt = """
An entity is defined an anatomical feature, a quantitative trait, a physical characteristic, or any descriptive term.
- Anatomical Feature: a specific part of an organism's body with a distinct structure and function. Examples: postrostral head shields, precloacal pores, nasal structure.
- Quantitative Trait: a measurable property of an organism. This can include dimenstions, numbers of body parts, or any other quantifiable aspect. Examples: body length, number of scales, number of body segments, number of body annuli, number of caudal annuli, weight.
- Physical Characteristic: a non-measurable trait that describes the physical appearance. Examples: skin texture, tail shape, postmalar chin shields, body color, tail color, dorsal color, irregular blotches.
- Descriptive Term: a term that isn't an anatomical feature, quantitative trait, or physical characteristic but has descriptors. Examples: location of a body part, location of a segment, or description of something else

Exclusions: 
- Species, family, order, dates, times, persons, references, lack of features, verbs, background information and non-specific descriptions are not considered entities,

Prompt structure:
- Entity identification: Clearly identify the entity without descriptors. It's an entity only if it's an anatomical feature, quantitative trait, physical characteristic, or descriptive term.
- Descriptor classification: After the entity, provide any relevant descriptors. If no specific descriptor applies, use "Not Applicable" to indicate this. Ensure that descriptors are specific and directly related to the entity.
- True/False Justification: Indicate whether the entity with its descriptor(s) fits the definition of being an entity (True) or not (False).
- Handling Ambiguities: In cases of ambiguity, prioritize the classification based on the primary function or most prominent characteristic of the entity.
- Standardized Vocabulary: Pull terms and descriptors directly from the description.

Amphisbaena innocens Sauria Amphisbaenidae DESCRIPTION: Size large (SVL to 262 mm); tail to 18 mm, conical, rounded terminally; no caudal autotomy; body annuli 186-219, caudal annuli 10-15; dorsal segments 14-17/midbody annulus, ventral segments 18-22/midbody annulus; 3 rows of postgenials; no postmalar chin shields;  4-6 (strongly modally 4) precloacal pores; nasal suture rather long but less than one-half length of prefrontal suture; 1 temporal. Dorsum (as preserved) shades of brown, at times with dark violet head and tail, grading to chocolate brown on body; color solid on head and tail, on body rectangular centers of each segment much darker than margins, giving the impression of dark spots; color darker dorsally than ventrally but no white segments (Schwartz & Henderson 1991: 560). For a discussion of geographic variation see Gans & Alexander 1962: 101.

Answer:
1. Amphisbaena innocens | Not Applicable | False | species.
2. Sauria | Not Applicable | False | order.
3. Amphisbaenidae | Not Applicable | family.
4. Size | no adjective | False | irrelevant.
5. SVL | 262 mm | True | quantitative.
6. tail | 18 mm | True | quantitative.
7. Tail shape | conical, rounded terminally | True | physical.
8. caudal autotomy | Not Applicable | False | lack of a feature.
9. body annuli | 186-219 | True | quantitative.
10. caudal annuli | 10-15 | True | quantitative.
11. dorsal segments/midbody annulus | 14-17 | True | quantitative.
12. ventral segments/midbody annulus | 18-22 | True | quantitative.
13. rows of postgenials | 3 | True | quantitative.
14. postmalar chin shields | Not Applicable | lack of a feature.
15. precoacal pores | 4-6 | True | quantitative.
16. nasal suture | rather long | True | anatomical.
17. temporal | 1 | True | quantitative.
18. Dorsum color | shades of brown | True | color.
19. head | dark violet | True | color.
20. tail | dark violet | True | color.
21. Body color | chocolate brown | True | color.
22. color on head | solid | True | color.
23. color on tail | solid | True | color.
24. Dorsal color | darker dorsally than ventrally | True | color.
25. white segments | Not Applicable | False | lack of a feature.
"""