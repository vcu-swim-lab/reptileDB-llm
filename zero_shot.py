from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


class TraitsExtractor:
    def __init__(self):
        self.llm = OpenAI(temperature=0.0, max_tokens=500)

    def get_traits(self):
        prompt_trait_template = PromptTemplate(
            input_variables=['diagnosis'],
            template="""
                        Given a diagnosis of a species, create a vertical numbered list of all its traits.
                        Diagnosis: {diagnosis}
                        Traits: 
                    """
        )

        traits_chain = LLMChain(
            llm=self.llm,
            prompt=prompt_trait_template,
            verbose=True
        )

        return traits_chain
