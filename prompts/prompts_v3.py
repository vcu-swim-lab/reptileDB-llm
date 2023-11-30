EXTRACT_TRAITS_PROMPT_V3 = """
                        I am working on a text span classification task for text describing reptiles. Your task is to
                        identify reptile characteristics that define the reptiles mentioned in the abstract.
                        
                        Abstract: {abstract}
                        
                        Each text span must be in the abstract. Provide output in the following format: 
                        "characteristic 1; characteristic 2; characteristic 3; ..."
                        
                        Include all relevant text that describe the reptile, including quantitative and 
                        qualitative descriptors."""

CATEGORIES_PROMPT_V3 = """                    
                    Abstract: {abstract}
                    
                    Characteristics: {characteristics}
                    
                    For each of these reptile characteristics, list the trait category it belongs to. The trait
                    category must be in the abstract.
                    
                    Provide output in the following format: "category 1, category 2, category 3, ..."
                    
                    Consider this example:
                    Abstract Input: "Achalinus spinalis Diagnosis (genus): (1) maxillary teeth 20–22, small,
                    equal; (2) mandibular teeth equal; (3) head not or only scarcely distinct from
                    neck; (4) eye small or moderate, with round or vertically subelliptical pupil;
                    (5) nostril in the anterior part of a large concave nasal, divided by a vertical
                    suture; (6) the loreal extending from the nasal to the eye; (7) body slender,
                    cylindrical; (8) dorsal scales in 23 rows, keeled; (9) subcaudals single."
                    
                    Characteristics Input: "maxillary teeth 20–22, small,
                    equal; mandibular teeth equal; head not or only scarcely distinct from
                    neck; eye small or moderate, with round or vertically subelliptical pupil; 
                    nostril in the anterior part of a large concave nasal, divided by a vertical
                    suture; the loreal extending from the nasal to the eye; body slender,
                    cylindrical; dorsal scales in 23 rows, keeled; subcaudals single."
                    
                    Trait categories output: "maxillary teeth, mandibular teeth, head, eye, nostril, 
                    loreal, body, dorsal scales, subcaudals"
                    
                    Ensure that the output is lowercase and does not include descriptors of the categories.
                    """