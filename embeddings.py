from openai import OpenAI
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import sys

client = OpenAI(api_key="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")

def tokenTraits(as_is_trait_count_file):
   df = pd.read_csv(as_is_trait_count_file) ##traitCount is the as_is_trait_counts_~~~~ file
   return df['trait'].tolist()

def tryout(trait_list, threshold = 0.8):
   similar_word_dict = {}
   key_words = []

   for trait in trait_list:
      if len(key_words) == 0:
         key_word = trait
         similar_word_dict[key_word] = []
         key_words.append(key_word)
      else:
         similar = False
         for key_word in key_words:
            similarity = calculateSimilarity(key_word, trait)
            if similarity >= threshold:
               similar = True
               similar_word_dict[key_word].append(trait)
               break
         if not similar:
            similar_word_dict[trait] = []
            key_words.append(trait)
   return similar_word_dict

##checks similarity between two traits
def calculateSimilarity(word1, word2):
   embed1 = client.embeddings.create(input=word1, model="text-embedding-3-large").data[0].embedding
   embed2 = client.embeddings.create(input=word2, model="text-embedding-3-large").data[0].embedding

   return cosine_similarity([embed1], [embed2])[0][0]

def main(as_is_trait_count_file):
   # Get trait list from the CSV file
   trait_list = tokenTraits(as_is_trait_count_file)

   # Combine terms and get new terms
   new_terms = tryout(trait_list)

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