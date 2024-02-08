step_one = """You are tasked with analyzing a text dataset that contains information 
about various reptile families, along with their characteristics and the frequency of each characteristic's 
occurrence. There should be no other information besides the knowledge you're told to give below.

Rank the characteristics based on their frequency of occurrence in descending order, 
with the most common characteristic labeled as '1', the second most common characteristic labeled as '2', and so on. 
Proceed up to the 30th most common characteristic. Alongside each characteristic should be its number of occurrences. 
For instance, [rank]. [characteristic], [frequency]. Only output the ranked list.
"""

step_two = """Your task involves analyzing a dataset that contains various characteristics of reptiles. Start by 
examining the dataset to identify characteristics that are similar or related to each other. Once you've identified 
these similarities, group related characteristics together. After grouping, update the count for each characteristic 
group to reflect the total number of occurrences of all characteristics within that group.

Your goal is to create a new list that includes the top 20 characteristic groups. This list should rank the groups 
based on their updated counts, with the groups having the highest counts at the top.

Follow this format for your final list:

1. Grouped characteristic, updated count
2. Grouped characteristic, updated count
... 

Ensure your list is strictly formatted as shown, with each line consisting of a grouped characteristic followed by 
its updated count. The list should be ordered in descending order based on the count of occurrences, starting with 
the most frequent characteristic group.

Do not include any additional explanations, notes, or deviations from the specified format in your final list.
"""