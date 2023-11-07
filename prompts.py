EXTRACT_TRAITS_PROMPT = """
                        Given the {diagnosis} of a species, identify the species name and extract its characteristics.
                        Format the output like this: "species name: characteristics"
                """

CATEGORIES_PROMPT = """
                    Given the {characteristics} of a species, categorize each into trait categories. 

                    Provide the ideal output in the format: (species): (characteristic) <(trait category)>, 
                    (characteristic) <(trait category)>, ...

                    Ensure that the trait category is in angled brackets <>

                    Here is an example:
                    Characteristics: "Cylindrophis ruffus; Characteristics: 19 midbody 
                    scale rows, 186–197 ventrals, wide and constant bands encircling dark body, an interrupted and 
                    wide band on the nape. "

                    Ideal Output: "Cylindrophis ruffus: 19 midbody scale rows <midbody scale rows>, 
                    186-197 ventrals <ventrals>, wide and constant bands encircling dark body <body bands>, 
                    interrupted and wide band on the nape <nape band>"
                    """
