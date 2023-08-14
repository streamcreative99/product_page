import streamlit as st
from langchain.llms import OpenAI

st.set_page_config(page_title='🦜🔗 Product Page App')
st.title('🦜🔗 Product Page App')

# Check for OpenAI API Key in Streamlit's secrets
if 'OPENAI_API_KEY' in st.secrets:
    st.sidebar.success('API key successfully loaded from secrets!', icon='✅')
    openai_api_key = st.secrets['OPENAI_API_KEY']
else:
    openai_api_key = st.sidebar.text_input('Enter OpenAI API Key:', type='password')

def generate_website_content(uploaded_files, openai_api_key):
    # Combine all uploaded documents into one string
    combined_document = " ".join([file.read().decode() for file in uploaded_files])
    
    # Define the prompt
    prompt = f"""
    {combined_document}
    Could you act as an SEO expert? Using the same tone and voice I provided, could you write a website page that is SEO optimized and informative?
    Please use the following Subheadings:
    PRODUCT DESCRIPTION - this section needs to consist of 2 Brief Paragraphs.
    FEATURES AND BENEFITS - this section needs to consist of only bullets
    APPLICATIONS - this section needs to consist of only bullets
    PERFORMANCE - this section needs to consist of only bullets
    """
    
    # Use OpenAI to generate the content
    llm = OpenAI(model_name='text-davinci-003', openai_api_key=openai_api_key)
    response = llm(prompt)
    return response

# File upload (multiple files allowed)
uploaded_files = st.file_uploader('Upload documents', type='txt', accept_multiple_files=True)

# Content generation and display
if uploaded_files:
    with st.form('myform'):
        submitted = st.form_submit_button('Generate Website Content')
        if submitted and openai_api_key.startswith('sk-'):
            with st.spinner('Generating content...'):
                content = generate_website_content(uploaded_files, openai_api_key)
                st.subheader("Generated Website Content:")
                st.write(content)
