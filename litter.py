import streamlit as st
from langchain_groq import ChatGroq
import streamlit as st
from langchain.output_parsers import StructuredOutputParser, ResponseSchema


groq_api_key = st.secrets["api"]

response_schema = [
    ResponseSchema(name="Yoruba translation", description="This is the Yoruba translation of the user's English input")
]
parser = StructuredOutputParser.from_response_schemas(response_schema)

def translator(query):
    llm_model = ChatGroq(api_key=groq_api_key, model="llama3-70b-8192")
    
    prompt = f"""You are a chatbot that translates user input (in English) to Yoruba.
    Follow the given structured format:
    {parser.get_format_instructions()}
    
    English text: {query}"""
    
    response = llm_model.invoke(prompt)
    
    if not response or not response.content.strip():
        return "Error: Received an empty response from LLM"
    
    try:
        parsed_response = parser.parse(response.content)
        return parsed_response["Yoruba translation"]
    except Exception as e:
        return f"Parsing failed: {e}"

st.title("English to Yoruba Translator")
st.markdown("Enter an English sentence, and the AI will translate it into Yoruba.")

user_input = st.text_area("Enter text in English:", "")

if st.button("Translate"):
    if user_input.strip():
        translation = translator(user_input)
        st.success("Translation:")
        st.write(translation)
    else:
        st.warning("Please enter some text to translate.")
