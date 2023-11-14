EXTRACT_TRAITS_PROMPT = """
                        I am working on a text span classification task for text describing reptiles. Your task is to
                        identify reptile characteristics that define the reptiles mentioned in the abstract.
                        
                        Abstract: {abstract}
                        
                        Each characteristic must be in the abstract. Provide output in the following format: 
                        "species name: characteristic 1; characteristic 2; characteristic 3; ..."
                        
                        Include all relevant text that describe the reptile, including quantitative and 
                        qualitative descriptors."""

CATEGORIES_PROMPT = """
                    Given reptile characteristics, your task is to list the trait category each characteristic 
                    belongs to in angled brackets. The trait category must be inferred from the list of characteristics 
                    given to you, not made up.
                    
                    Characteristics: {characteristics}
                    
                    Provide output in the following format: 
                    "species name: characteristic 1 <trait category>, characteristic 2 <trait category>, ..."
                        
                    Consider this example:
                
                    Characteristics: "Cylindrophis ruffus: 19 midbody scale rows; 186–197 ventrals; wide and constant 
                    bands encircling dark body; an interrupted and wide band on the nape."

                    Output: "Cylindrophis ruffus: 19 midbody scale rows <midbody scale rows>, 
                    186-197 ventrals <ventrals>, wide and constant bands encircling dark body <body bands>, 
                    interrupted and wide band on the nape <nape band>."
                    """

