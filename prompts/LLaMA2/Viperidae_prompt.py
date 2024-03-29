"""Our current prompt for Viperidae LLaMa2"""

prompt_vipers = """Defn: An entity is an anatomical feature of an organism(anatomical), a measurable quantitative trait(quantitative), a physical characteristic that describes appearance(physical), or a lack of a feature (lackofafeature). Species, geography, family, order, dates, times, persons, references, verbs, and general background information are not entities. Species, family, order, dates, times, persons, references, verbs, and general background information are not entities.

Q: Given the paragraph below, identify a list of possible entities and for each entry explain why it either is or is not an entity:

Paragraph: Daboia russelii	Serpentes	Viperidae	Diagnosis: No sensory pit between nostril and eye; head very distinct from 
neck, above covered by small, keeled, imbricate scales, 6–9 between narrow supraoculars; nostril large, 
in large nasal shield which, below, is fused to the rostral; eye, with vertically elliptic pupil, surrounded by 10–15 
small scales, 3–4 rows of small scales separating the circumocular scales from the upper labials; temporals small; 
10–12 upper labials; 27–33 longitudinal rows of scales at midbody, all except outmost row strongly keeled; ventrals 
153–180; subcaudals 41–64, all paired; color above light brown with 3 longitudinal series of large black-margined 
brown spots or blotches, the vertebral series often merging to form a chain-like longitudinal stripe, occasionally an 
additional longitudinal series of small dark spots between vertebral and lateral series; yellowish white below 
occasionally with dark brown markings. Total length to 1600 mm are not uncommon (fide Smith 1943:484). Check Figure 5 [after LEVITON 
2003]

Answer:
1. Daboia russelii | Not Applicable | False | species (species).
2. Serpentes | Not Applicable | False | order (order).
3. Viperidae | Not Applicable | False | family (family).
4. sensory pit | No | True | lack of a feature (lackofafeature).
5. head distinction from neck | very distinct | True | physical (physical).
6. head scales | above covered by small, keeled, imbricate scales | True | physical (physical).
7. scales between supraoculars | 6–9 | True | quantitative (quantitative).
8. nostril size | large | True | physical (physical).
9. nasal shield | nostril, in large nasal shield which, below, is fused to the rostral | True | physical (physical).
10. pupil shape | vertically elliptic | True | physical (physical).
11. circumocular scales | surrounded by 10–15 small scales | True | quantitative (quantitative).
12. Scales between circumocular and upper labials | 3–4 rows of small scales separating the circumocular scales from the upper labials | True | quantitative (quantitative).
13. temporals | small | True | physical (physical).
14. upper labials | 10–12 | True | quantitative (quantitative).
15. longitudinal rows of scales at midbody | 27–33 | True | quantitative (quantitative).
16. scale keeling | all except outmost row strongly keeled | True | physical (physical).
17. ventrals | 153–180 | True | quantitative (quantitative).
18. subcaudals | 41–64, all paired | True | quantitative (quantitative).
19. color above | light brown with 3 longitudinal series of large black-margined brown spots or blotches | True | physical (physical).
20. vertebral series | often merging to form a chain-like longitudinal stripe | True | physical (physical).
21. additional spots | occasionally an additional longitudinal series of small dark spots between vertebral and lateral series | True | physical (physical).
22. color below | yellowish white below occasionally with dark brown markings | True | physical (physical).
23. total length | to 1600 mm | True | quantitative (quantitative).
24. Smith 1943:484 | Not Applicable | False | reference.
25. Figure 5 | Not Applicable | False | reference.
26. LEVITON 2003 | Not Applicable | False | reference.
"""