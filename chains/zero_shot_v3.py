from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from prompts.prompts_v3 import EXTRACT_TRAITS_PROMPT_V3, CATEGORIES_PROMPT_V3


class TraitsExtractorV3:
    def __init__(self):
        self.llm = OpenAI(temperature=0.0)
        self.categorize_traits_chain = self.categorize_characteristics()
        self.extract_traits_chain = self.get_traits()

    def get_traits(self):
        prompt_trait_template = PromptTemplate(
            input_variables=['abstract'],
            template=EXTRACT_TRAITS_PROMPT_V3
        )

        extract_traits_chain = LLMChain(
            llm=self.llm,
            prompt=prompt_trait_template,
            output_key='characteristics',
            verbose=True
        )

        return extract_traits_chain

    def categorize_characteristics(self):
        prompt_categorize_template = PromptTemplate(
            input_variables=['abstract', 'characteristics'],
            template=CATEGORIES_PROMPT_V3,
        )

        categorize_traits_chain = LLMChain(
            llm=self.llm,
            prompt=prompt_categorize_template,
            output_key='trait_categories',
            verbose=True
        )

        return categorize_traits_chain

    def get_categorized_traits(self):
        overall_chain = SequentialChain(
            chains=[self.extract_traits_chain, self.categorize_traits_chain],
            input_variables=['abstract'],
            verbose=True
        )

        return overall_chain
