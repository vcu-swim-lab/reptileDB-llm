prompt_summarize = """You are tasked with analyzing a text dataset that contains information about various reptile 
families, along with their characteristics and the frequency of each characteristic's occurrence. To summarize this 
data, perform the following steps:

Step 1: Characteristic Ranking: Rank the characteristics based on their frequency of occurrence in descending order, 
with the most common characteristic labeled as '1', the second most common characteristic labeled as '2', and so on. 
Proceed up to the 30th most common characteristic. Alongside each characteristic should be its number of occurrences. 
For instance, "1. ventrals, 15". Only output the ranked list at this step.

Step 2: Grouping Synonymous Characteristics: Group synonymous characteristics or ones that are more detailed 
versions of others from the text dataset, and update the new counts. Create a new ordered list with the updated counts.
Output this ordered list in the same format as step 1.

Do not ask any questions or give any irrelevant information. Perform each step in order.

Read the instructions again: You are tasked with analyzing a text dataset that contains information about various reptile 
families, along with their characteristics and the frequency of each characteristic's occurrence. To summarize this 
data, perform the following steps:

Step 1: Characteristic Ranking: Rank the characteristics based on their frequency of occurrence in descending order, 
with the most common characteristic labeled as '1', the second most common characteristic labeled as '2', and so on. 
Proceed up to the 30th most common characteristic. Alongside each characteristic should be its number of occurrences. 
For instance, "1. ventrals, 15". Only output the ranked list at this step.

Step 2: Grouping Synonymous Characteristics: Group synonymous characteristics or ones that are more detailed 
versions of others from the text dataset, and update the new counts. Create a new ordered list with the updated counts.
Output this ordered list in the same format as step 1.

Do not ask any questions or give any irrelevant information. Perform each step in order."""