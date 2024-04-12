from openai import OpenAI
import pandas as pd
from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity
import sys

client = OpenAI(api_key="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")

def tokenTraits(as_is_trait_count_file):
   trait_list = []
   df = pd.read_csv(as_is_trait_count_file) ##traitCount is the as_is_trait_counts_~~~~ file
   for _, row in df.iterrows(): ##iterates over each row 
      trait = row['trait'] ##extract value from trait column
      trait_list.append(trait)
   return trait_list
         
      
def combine_terms(trait_list, threshold=0.8):
   new_terms = []
   for term1, term2 in combinations(trait_list, 2):
      # Create embeddings
      response1 = client.embeddings.create(input=term1, model="text-embedding-3-large")
      response2 = client.embeddings.create(input=term2, model="text-embedding-3-large")
      embed1 = response1.data[0].embedding
      embed2 = response2.data[0].embedding

      # Calculate similarities
      similarity = cosine_similarity([embed1], [embed2])[0][0]
        
      # Check for threshold
      if similarity > threshold:
         combined_embedding = [(x + y) / 2 for x, y in zip(embed1, embed2)]  # Create a new embedding
         response = client.embeddings.create(input=combined_embedding, model="text-embedding-3-large")
         new_term = response.data[0].embedding
         ##generate into text???
         # Check if the new term is not already associated with a term in new_terms
         if not any(new_term in term for term in new_terms):
            new_terms.append(new_term)
   return new_terms


def main(as_is_trait_count_file):
   # Get trait list from the CSV file
   trait_list = tokenTraits(as_is_trait_count_file)

   # Combine terms and get new terms
   new_terms = combine_terms(trait_list)

   # Generate HTML content with new terms
   html_content = "<html><body><h1>New Terms</h1><ul>"
   for term in new_terms:
      html_content += f"<li>{term}</li>"
   html_content += "</ul></body></html>"

   # Write HTML content to file
   with open("new_terms.html", "w") as file:
      file.write(html_content)

if __name__ == "__main__":
   if len(sys.argv) != 2:
      print("Usage: python script_name.py as_is_trait_counts_file.csv")
      sys.exit(1)
   main(sys.argv[1])