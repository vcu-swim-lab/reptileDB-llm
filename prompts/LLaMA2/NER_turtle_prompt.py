prompt = """
An entity is an anatomical feature of an organism (anatomical), a measurable quantitative trait (quantitative), a physical characteristic that describes appearance (physical). Species, subspecies, family, order, dates, times, persons, references, verbs, and general background information are not entities.

Elusor macrurus	Diagnosis (Genus). A short-necked Australian chelid turtle oflarge adult size, with a low streamlined 
shell, basking habits, and a southern temperate breeding pattern. Distinguished from all other Australian chelid 
turtles by the following combination of characters (characters marked with an asterisk [*] are alone diagnostic): 1. 
Eye dull and dark with a vestigial nictitating membrane*. 2. Barbels long and fleshy. 3. Humerus and femur of 
subequallength*. 4. Inguinal and axillary buttresses of subequal size*. 5. Precentral [nuchal] scute always present. 
6. Tail distinctive (all sexes and ages) in having a large precloacal portion*, a longitudinal, slitlike cloacal 
orifice*, and in being laterally compressed*. 7. Distal caudal vertebrae much higher than long and bearing distinct 
haemal arches*. 8. Length of tail in adult males more than half length of carapace and significantly longer than 
combined length of head and neck*.

Answer:
1. Elusor macrurus | Not Applicable | False | species.
2. Neck | short-necked | True | physical.
3. Size | large | True | physical.
4. Shell | low streamlined | True | physical.
5. Habits | basking | True | descriptive.
6. Breeding pattern | southern temperate | True | descriptive.
7. Eye | dull and dark with a vestigial nictitating membrane | True | physical.
8. Barbels | long and flashy | True | physical.
9. Inguinal and axillary buttresses | of equal size | True | physical.
10. Precentral [nuchal] scute | always present | True | physical.
11. Tail | distinctive (all sexes and ages) in having a large precloacal portion | True | physical.
12. cloacal orifice | longitudinal, slitlike | True | physical.
13. laterally compressed | Not Applicable | False | not descriptive.
14. Distal caudal vertebrae | much higher than long and bearing distinct haemal arches | True | physical.
15. Length of tail | in adult males more than half length of carapace and significantly longer than combined length of head and neck | True | quantitative.

Cuora aurocapitata	Description. As the common name indicates, the head is bright yellow on top. The carapace does not 
exceed 120 mm in length and is rather flat, without posterior serration. The carapace is a uniform dark brown, 
and the plastron yellow and lacking an anal notch. The plastral hinge is well developed and fully mobile, 
and the raised lobes are able to close the shell openings completely. The head is of medium size, pointed, 
black or grayish below and on the neck, with light areas on the mandibles and the sides and with a brilliant yellow 
shield or helmet on top. The forelimbs bear strikingly enlarged scales. (Bonin 2006)

Answer:
1. Cuora aurocapitata | Not Applicable | False | species.
2. Head | bright yellow on top | True | physical.
3. carapace | does not exceed 120 mm in length and is rather flat, without posterior serration | True | physical. 
4. carapace color | uniform dark brown | True | physical.
5. plastron | yellow and lacking an anal notch | True | descriptive.
6. plastral hinge | well developed and fully mobile | True | physical.
7. raised lobed | are able to close the shell openings completely | True | physical.
8. head | medium size, pointed, black or grayish below and on the neck, with light areas on the mandibles and the sides and with a brilliant yellow shield or helmet on top | True | descriptive.
9. forelimbs | bear strikingly enlarged scales | True | physical.
10. Bonin 2006 | Not Applicable | False | reference.

Kinixys nogueyi	Description: “K. b. nogueyi (Lataste, 1886) occurs in West Africa from Senegal eastward to Cameroon 
and the Central African Republic. This subspecies has only four claws on each forefoot, the pectoral midseam 28-39% 
of the length of the combined gular and humeral midseams and 22-36% of the abdominal midseam, and a domed carapace (
length/height ratio < 2.3) which is uniformly brown or with yellow areolae bordered with dark pigment.” (Ernst & 
Barbour 1989: 230)

Answer:
1. Kinixys nogueyi | Not Applicable | False | species.
2. K. b. nogueyi | Not Applicable | False | subspecies.
3. Lataste, 1886 | Not Applicable | False | reference.
4. West Africa from Senegal | eastward to Cameroon and the Central African Republic | False | general background information.
5. forefoot | four claws | True | quantitative.
6. pectoral midseam | of the length of the combined gular and humeral midseams and 22-36% of the abdominal midseam | True | quantitative.
7. carapace | domed (length/height ratio < 2.3) which is uniformly brown or with yellow areolae bordered with dark pigment | True | descriptive.
8. Ernst & Barbour 1989: 230 | Not Applicable | False | reference.
"""