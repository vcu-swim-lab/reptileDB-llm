EXTRACT_TRAITS_PROMPT_V2 = """
                        I am working on a text span classification task for text describing reptiles. Your task is to
                        identify reptile characteristics that define the reptiles mentioned in the abstract.

                        Abstract: {abstract}

                        Each characteristic must be in the abstract. Provide output in the following format: 
                        "species name: characteristic 1; characteristic 2; characteristic 3; ..."

                        Include all relevant text that describe the reptile, including quantitative and 
                        qualitative descriptors.
                        """

CATEGORIES_PROMPT_V2 = """
                    Given reptile characteristics, your task is to list the trait category each characteristic 
                    belongs to in angled brackets. The trait category must be in the list of categories given to you.
                    
                    Characteristics: "{characteristics}"

                    Here are the trait categories to use: <axilla-groin length>, <axilla-groin scales>, <arm width>, 
                    <anal plate>, <apical pits>, <parietal angle>, <apical scales>, <anal plate size>, <auricular 
                    lobes>, <collar scales>, <caudal ribs>, <chin shields>, <collar-snout length>, 
                    <caudal vertebrae>, <dorsal scale rows>, <dorsal scales>, <dorsal tubercles>, <temporal 
                    markings>, <femoral scales>, <ear size>, <eye size>, <eye-ear distance>, <eye-nostril distance>, 
                    <femur length>, <forelimb length>, <foot length>, <femoral pores>, <frontal scales>, 
                    <flank scales>, <frontal-snout length>, <gular scales>, <head scales>, <head size>, 
                    <hindlimb length>, <humerus length>, <head width>, <interdigital scales>, <infralabials>, 
                    <interlimb length>, <internasals>, <interorbital distance>, <jaw size>, <dorsal scale keels>, 
                    <supralabial size>, <digit lamellae>, <tail lamellae>, <lower tail scales>, <mental scale>, 
                    <midbody size>, <maxillary teeth>, <metatarsal length>, <neck size>, <nostril scale>, 
                    <nuchal scales>, <orbital diameter>, <chin shields pairs>, <palm length>, <parietals>, 
                    <pileus color>, <preanal pores>, <preocular scale>, <postmentals>, <postnasal scale>, 
                    <postoculars>, <precloacal scales>, <preventrals>, <rostral scale>, <supralabials>, 
                    <snout scales>, <snout-vent length>, <tail size>, <temporal scales>, <tubercle rows>, 
                    <tympanum size>, <ventral scales>, <vertebral spots>
                    
                    Provide output in the following format: "species name: characteristic 1 <trait category 1>, 
                    characteristic 2 <trait category 2>, ..."
                    
                    Consider this example:
                    
                    Characteristics: "Cylindrophis ruffus: 19 midbody scale rows; 186–197 ventrals; wide and constant 
                    bands encircling dark body; an interrupted and wide band on the nape."

                    Output: "Cylindrophis ruffus: 19 midbody scale rows <midbody scale rows>, 
                    186-197 ventrals <ventrals>, wide and constant bands encircling dark body <body bands>, 
                    interrupted and wide band on the nape <nape band>."
                    """