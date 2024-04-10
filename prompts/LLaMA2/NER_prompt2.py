"""Our current prompt for Llama2 non-turtle descriptions"""

prompt = """Defn: An entity is an anatomical feature of an organism(anatomical), a measurable quantitative trait(quantitative), a physical characteristic that describes appearance(physical), or a lack of a feature (lackofafeature). Species, family, order, geography, dates, times, persons, references, verbs, and general background information are not entities.

Q: Given the paragraph below, identify a list of possible entities and for each entry explain why it either is or is not an entity:

Paragraph: Amphisbaena innocens Sauria Amphisbaenidae DESCRIPTION: Size large (SVL to 262 mm); tail to 18 mm, conical, 
rounded terminally; no caudal autotomy; body annuli 186-219, caudal annuli 10-15; dorsal segments 14-17/midbody 
annulus, ventral segments 18-22/midbody annulus; 3 rows of postgenials; no postmalar chin shields;  4-6 (strongly 
modally 4) precloacal pores; nasal suture rather long but less than one-half length of prefrontal suture; 1 temporal. 
Dorsum (as preserved) shades of brown, at times with dark violet head and tail, grading to chocolate brown on body; 
color solid on head and tail, on body rectangular centers of each segment much darker than margins, giving the 
impression of dark spots; color darker dorsally than ventrally but no white segments (Schwartz & Henderson 1991: 
560). For a discussion of geographic variation see Figure 5 Gans & Alexander 1962: 101.

Answer:
1. Amphisbaena innocens | Not Applicable | False | species (species).
2. Sauria | Not Applicable | False | order (order).
3. Amphisbaenidae | Not Applicable | False | family (family).
4. Size | large (SVL to 262 mm) | True | quantitative (quantitative).
5. SVL | to 262 mm | True | quantitative (quantitative).
6. tail length | to 18 mm | True | quantitative (quantitative).
7. tail shape | conical, rounded terminally | True | physical (physical).
8. caudal autotomy | no | True | lack of a feature (lackofafeature).
9. body annuli | 186-219 | True | quantitative (quantitative).
10. caudal annuli | 10-15 | True | quantitative (quantitative).
11. dorsal segments | 14-17/midbody annulus | True | quantitative (quantitative).
12. ventral segments | 18-22/midbody annulus | True | quantitative (quantitative).
13. postgenials | 3 rows | True | quantitative (quantitative).
14. postmalar chin shields | no | True | lack of a feature (lackofafeature).
15. precloacal pores | 4-6 (strongly modally 4) | True | quantitative (quantitative).
16. nasal suture length | rather long but less than one-half length of prefrontal suture | True | quantitative (quantitative).
17. temporal | 1 | True | quantitative (quantitative).
18. Dorsum color | shades of brown, at times with dark violet head and tail, grading to chocolate brown on body | True | physical (physical).
19. body color pattern | color solid on head and tail, on body rectangular centers of each segment much darker than margins, giving the impression of dark spots | True | physical (physical).
20. Color contrast | color darker dorsally than ventrally but no white segments | True | physical (physical).
21. (Schwartz & Henderson 1991: 560) | Not Applicable | False | reference.
22. Figure 5 | Not Applicable | False | reference.
23. Gans & Alexander | Not Applicable | False | reference.
"""