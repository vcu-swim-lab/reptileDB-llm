from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from prompts.prompts_v2 import EXTRACT_TRAITS_PROMPT_V2, CATEGORIES_PROMPT_V2


class TraitsExtractorV2:
    def __init__(self):
        self.llm = OpenAI(temperature=0.0)
        self.categorize_traits_chain = self.categorize_characteristics()
        self.extract_traits_chain = self.get_traits()

    def get_traits(self):
        prompt_trait_template = PromptTemplate(
            input_variables=['diagnosis'],
            template=EXTRACT_TRAITS_PROMPT_V2
        )

        extract_traits_chain = LLMChain(
            llm=self.llm,
            prompt=prompt_trait_template,
            verbose=True
        )

        return extract_traits_chain

    def categorize_characteristics(self):
        prompt_categorize_template = PromptTemplate(
            input_variables=['characteristics'],
            template=CATEGORIES_PROMPT_V2
        )

        categorize_traits_chain = LLMChain(
            llm=self.llm,
            prompt=prompt_categorize_template,
            verbose=True
        )

        return categorize_traits_chain

    def get_categorized_traits(self):
        overall_chain = SimpleSequentialChain(
            chains=[self.extract_traits_chain, self.categorize_traits_chain], verbose=True
        )

        return overall_chain
