EXTRACT_TRAITS_PROMPT = """
                        Given the {diagnosis} of a species, identify the species name and extract its characteristics.
                        Format the output like this: "species name: characteristics"
                """

CATEGORIES_PROMPT = """
                    Given the {characteristics} of a species, categorize each into trait categories. 
                    
                    Provide the ideal output in the format: (species): (characteristic) <(trait category)>, 
                    (characteristic) <(trait category)>, ...
                    
                    Ensure that the trait category is in angled brackets <>
                    
                    Here are some examples of trait categories: midbody scale, rows, ventrals, body bands, nape band,
                    subocular scale, prefrontal-orbit, contact, supralabials, infralabials, subcaudals, 
                    ventral blotches, prefrontal lateral blotches, SVL, dorsal scales, anal, loreal, and more.                                            
                  """
