from openai import OpenAI as ai
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

ai.api_key = 'your_api_key'

def traitNamesList(traitNames): ##grabs the synonymous traits we count by
   df = pd.read_csv(traitNames) ##trait names synonyms file
   synonymous_names = []
   for index, row in df.iterrows():
      next(df) ##skip line 1
      token = row[1].strip().split(',') ##split by ,
      modified_token = [t.replace(';', '') for t in token] ##get rid of ; from each token
      embeddings = [ai.Embedding.create(input_text=modified_token)['embedding']] ##creates embeddings for all trait name synonyms in file
      synonymous_names.append(embeddings, modified_token) ##stores here
   return synonymous_names ##hopefully returns embeddings of all trait names + their counterpart

def traitCountList(traitCount, model="text-embedding-3-small"): ##embeddings turns the words into tokenized numerical values that can be mixed and matched
   df = pd.read_csv(traitCount) ##traitCount is the as_is_trait_counts_~~~~ file
   synonymous_groups = []
   results = []
   threshold = 0.8
   for _, row in df.iterrows(): ##iterates over each row 
      trait = row['trait'] ##extract value from trait column
      embeddings = [ai.Embedding.create(input_text=token)['embedding'] for token in trait] ##creates embeddings for all the traits inside as_is_trait_counts file
      synonymous_groups.append(embeddings) ##grabs into a list
      count = row['count']
      for num in count:
        for i, emb1 in enumerate(traitNamesList):
           for j, emb2 in enumerate(synonymous_groups):
              similarity_score = cosine_similarity([emb1], [emb2])[0][0]
              if similarity_score >= threshold:
                 results.append()