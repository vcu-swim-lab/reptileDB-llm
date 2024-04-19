from openai import OpenAI
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import sys

client = OpenAI(api_key="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")

def tokenTraits(as_is_trait_count_file):
   df = pd.read_csv(as_is_trait_count_file) ##traitCount is the as_is_trait_counts_~~~~ file
   return df['trait'].tolist()

def tryout(trait_list, threshold=0.6):
    similar_word_dict = {}

    for trait in trait_list:
        similar = False
        for key_word, similar_words in similar_word_dict.items():
            for word_group in similar_words:
                similarity = calculateSimilarity(key_word, trait)
                if similarity >= threshold:
                    word_group.append(trait)
                    similar = True
                    break
            if similar:
                break
        if not similar:
            similar_word_dict[trait] = [[trait]]  # Start a new group
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
    html_content = "<html><body><h1>Synonymous Terms Grouped</h1>"
    for key_word, similar_words in new_terms.items():
        html_content += f"<h2>{key_word}</h2><ul>"
        for word_group in similar_words:
            html_content += "<li>"
            html_content += ", ".join(word_group)
            html_content += "</li>"
        html_content += "</ul>"
    html_content += "</body></html>"

    # Write HTML content to file
    with open("synonymous_terms_list.html", "w") as file:
        file.write(html_content)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py as_is_trait_counts_file.csv")
        sys.exit(1)
    main(sys.argv[1])