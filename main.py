from dotenv import load_dotenv
import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

llm = OpenAI(openai_api_key=API_KEY, temperature=0.0)

prompt_trait = PromptTemplate(
    template=f"Given a description of a species, create a numbered list of all its traits: {{diagnosis}}",
    input_variables=['diagnosis']
)

traits_chain = LLMChain(
    llm=llm,
    prompt=prompt_trait,
    verbose=True
)

st.set_page_config(page_title="ReptileLLM")
st.title("🦎 ReptileLLM")

user_prompt = st.text_input("Enter the diagnosis")

if st.button("Get traits") and user_prompt:
    with st.spinner("Extracting traits..."):
        output = traits_chain.run(diagnosis=user_prompt)
        st.write(output)
