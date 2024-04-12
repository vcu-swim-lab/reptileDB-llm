from openai import OpenAI as ai
import pandas as pd
from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity
import sys

ai.api_key = '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'

def tokenTraits(as_is_trait_count_file):
   trait_list = []
   df = pd.read_csv(as_is_trait_count_file) ##traitCount is the as_is_trait_counts_~~~~ file
   for _, row in df.iterrows(): ##iterates over each row 
      trait = row['trait'] ##extract value from trait column
      trait_list.append(trait)
   return trait_list
         
      
def combine_terms(trait_list, threshold = 0.8):
   new_terms = []
   for term1, term2 in combinations(trait_list, 2):
      ##create embeddings
      embed1 = ai.Embedding.create(input_text=term1)['embedding']
      embed2 = ai.Embedding.create(input_text=term2)['embedding']

      ##calculate similarities
      similarity = cosine_similarity([embed1], [embed2])[0][0]

      ##check for threshold
      if similarity > threshold:
         combined_embedding = (term1 + term2)/2 ##creates a new embedding
         new_term = ai.Embedding.retrieve(closest_embedding=combined_embedding)['object']

         ##checks whether the new term created isn't already associated with a term already inside new_terms
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