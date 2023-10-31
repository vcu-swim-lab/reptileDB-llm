from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from prompts import TRAITS_PROMPT


class TraitsExtractor:
    def __init__(self):
        self.llm = OpenAI(temperature=0.0, max_tokens=500)

    def get_traits(self):
        prompt_trait_template = PromptTemplate(
            input_variables=['diagnosis'],
            template=TRAITS_PROMPT
        )

        traits_chain = LLMChain(
            llm=self.llm,
            prompt=prompt_trait_template,
            verbose=True
        )

        return traits_chain
