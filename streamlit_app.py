import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
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
    # Combine all uploaded files into one document
    combined_document = "\n\n".join([file.read().decode() for file in uploaded_files])

    # Split document into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    chunks = text_splitter.create_documents([combined_document])

    all_summaries = []
    llm = OpenAI(model_name='text-davinci-003', openai_api_key=openai_api_key)

    for chunk in chunks:
        # Get a summary of each chunk
        summary_prompt = f"Summarize the following text in 2-3 sentences:\n\n{chunk}"
        summary = llm(summary_prompt)
        all_summaries.append(summary)

    # Combine all summaries into one comprehensive summary
    comprehensive_summary = " ".join(all_summaries)

    # Define the final prompt using the comprehensive summary
    prompt = f"""
    {comprehensive_summary}
    Using the summarized document as a reference and maintaining its tone and voice, please craft an SEO-optimized and informative website page on the product...
    """

    # Generate the final content
    content = llm(prompt)

    return content

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
