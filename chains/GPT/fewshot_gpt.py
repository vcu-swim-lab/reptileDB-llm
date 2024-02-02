import openai
from prompts.gpt_prompt import prompt
from prompts.summarize_prompt_gpt import prompt_summarize


class TraitsExtractorGPT:
    def __init__(self, model_name):
        self.model_name = model_name

    def get(self, diagnosis):
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": diagnosis}
            ]
        )
        return response["choices"][0]["message"]["content"]

    def process(self, data):
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": prompt_summarize},
                {"role": "user", "content": data}
            ]
        )
        return response["choices"][0]["message"]["content"]
