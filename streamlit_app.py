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
    
    # Define the refined prompt
    prompt = f"""
    {combined_document}
    Using the uploaded document as a reference and maintaining its tone and voice, please craft an SEO-optimized and informative website page on the product. Structure the content as follows:
    - **Title**: A compelling title for the product.
    - **PRODUCT DESCRIPTION**: 2 concise paragraphs detailing the product, its design, and its main features.
    - **FEATURES AND BENEFITS**: A bulleted list highlighting the product's unique features and the benefits they offer.
    - **APPLICATIONS**: A bulleted list showcasing various use-cases and industries where the product can be applied.
    - **PERFORMANCE**: A bulleted list emphasizing the product's performance metrics, standards, and efficiency.
    Ensure the content is comprehensive, engaging, and effectively highlights the product's value proposition.
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
