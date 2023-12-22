from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from prompts.prompts_v3 import prompt


class TraitsExtractorV3:
    def __init__(self):
        self.llm = OpenAI(temperature=0.0)
        self.extract_traits_chain = self.get_traits()

    def get_traits(self):
        prompt_trait_template = PromptTemplate(
            input_variables=['abstract'],
            template=prompt
        )

        extract_traits_chain = LLMChain(
            llm=self.llm,
            prompt=prompt_trait_template,
            output_key='characteristics',
            verbose=True
        )

        return extract_traits_chain
