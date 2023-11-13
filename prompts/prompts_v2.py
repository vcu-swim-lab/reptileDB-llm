EXTRACT_TRAITS_PROMPT_V2 = """
                        Given the following diagnosis: 
                        
                        "{diagnosis}" 
                        
                        Identify the species name and extract its characteristics.
                        Format the output like this: "species name: characteristics"
                    """

CATEGORIES_PROMPT_V2 = """
                    Classify the the following species characteristics into trait categories.

                    Characteristics: "{characteristics}" 
                    
                    Provide the ideal output in the format: (species): (characteristic) <(trait category)>, 
                    (characteristic) <(trait category)>, ...

                    Ensure that the trait category is in angled brackets <>

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

                    Here is an example:
                    Characteristics: "Cylindrophis ruffus; Characteristics: 19 midbody 
                    scale rows, 186–197 ventrals, wide and constant bands encircling dark body, an interrupted and 
                    wide band on the nape. "

                    Ideal Output: "Cylindrophis ruffus: 19 midbody scale rows <midbody scale rows>, 
                    186-197 ventrals <ventrals>, wide and constant bands encircling dark body <body bands>, 
                    interrupted and wide band on the nape <nape band>"
                    """