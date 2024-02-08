step_one = """You are tasked with analyzing a text dataset that contains information 
about various reptile families, along with their characteristics and the frequency of each characteristic's 
occurrence. There should be no other information besides the knowledge you're told to give below.

Rank the characteristics based on their frequency of occurrence in descending order, 
with the most common characteristic labeled as '1', the second most common characteristic labeled as '2', and so on. 
Proceed up to the 30th most common characteristic. Alongside each characteristic should be its number of occurrences. 
For instance, [rank]. [characteristic], [frequency]. Only output the ranked list.
"""

step_two = """Your task is to analyze a dataset of reptile characteristics. Begin by identifying similar 
characteristics within the dataset and group them together. Once grouped, update the count for each characteristic to 
reflect the total occurrences across all grouped categories. Then, generate a new list that ranks these grouped 
characteristics by their updated counts in descending order, focusing specifically on the top 20 characteristics.

Format:
1. characteristic, count
2. characteristic, count
...

Ensure your final list strictly adheres to this format, without including any additional explanations or notes. The 
list should be ordered based on the count of occurrences, with the most frequent characteristic listed first.
"""