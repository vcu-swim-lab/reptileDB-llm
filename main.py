from dotenv import load_dotenv
import os
import streamlit as st
from zero_shot import TraitsExtractor

traits = TraitsExtractor()

load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']


def set_page_configuration():
    st.set_page_config(page_title="ReptileLLM")
    st.title("🦎 ReptileLLM")


def set_home_page():
    user_prompt = st.text_input("Enter the diagnosis")

    if st.button("Get traits") and user_prompt:
        with st.spinner("Extracting traits..."):
            output = traits.get_traits().run(user_prompt)
            st.write(output)
            print(output)


def main():
    set_page_configuration()
    set_home_page()


if __name__ == "__main__":
    main()
