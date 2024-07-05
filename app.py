import streamlit as st
import boto3
import json
import os

# Custom CSS to set font styling, remove rounded corners, and change hover colors
st.markdown("""
<style>
    /* Body text formatting */
    body {
        font-family: Menlo, ui-monospace, SFMono-Regular, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        font-weight: 100;
        font-size: 14px;
        line-height: 20px;
        color: rgb(255, 255, 255);
        background-color: black;
    }
    
    /* Ensure all text uses the specified font */
    * {
        font-family: Menlo, ui-monospace, SFMono-Regular, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important;
        font-weight: 100 !important;
    }
    
    /* Title formatting */
    h1 {
        font-size: 36px !important;
        line-height: 40px !important;
        font-weight: 100 !important;
    }
    
    /* Remove rounded corners */
    * {
        border-radius: 0 !important;
    }
    
    /* Style for chat input */
    .stChatInputContainer {
        border-radius: 0 !important;
    }
    .stChatInputContainer > div {
        border-radius: 0 !important;
    }
    .stChatInputContainer input {
        border-radius: 0 !important;
        font-family: Menlo, ui-monospace, SFMono-Regular, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important;
        font-weight: 100 !important;
    }
    
    /* Style for expanders */
    .streamlit-expanderHeader {
        border-radius: 0 !important;
    }
    .streamlit-expanderContent {
        border-radius: 0 !important;
    }
    
    /* Ensure chat messages have square corners and correct font */
    .stChatMessage {
        border-radius: 0 !important;
        font-family: Menlo, ui-monospace, SFMono-Regular, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important;
        font-weight: 100 !important;
    }

    /* Change hover color for links and expanders */
    a:hover, .streamlit-expanderHeader:hover {
        color: rgb(84, 232, 179) !important;
    }

    /* Change hover color for expander content */
    .streamlit-expanderContent:hover {
        color: rgb(84, 232, 179) !important;
    }
</style>
""", unsafe_allow_html=True)

region = boto3.Session().region_name
session = boto3.Session(region_name=region)
lambda_client = session.client('lambda')

st.title("LymeGPT")

sessionId = ""

# Initialize chat history and session id
if "messages" not in st.session_state:
    st.session_state.messages = []
if 'sessionId' not in st.session_state:
    st.session_state['sessionId'] = sessionId

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask about Lyme disease treatment..."):
    st.chat_message("user").markdown(prompt)

    # Call lambda function to get response from the model
    payload = json.dumps({"question": prompt, "sessionId": st.session_state['sessionId']})
    result = lambda_client.invoke(
        FunctionName='InvokeKnowledgeBase',
        Payload=payload
    )

    result = json.loads(result['Payload'].read().decode("utf-8"))
    answer = result['body']['answer']
    sessionId = result['body']['sessionId']
    citations = result['body']['citations']

    st.session_state['sessionId'] = sessionId
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(answer)
        
        st.markdown("### Sources:")
        chunk_counter = 1
        displayed_chunks = set()  # To keep track of displayed chunks

        for citation in citations:
            for reference in citation['retrievedReferences']:
                chunk_text = reference['content']['text']
                s3_location = reference['location']['s3Location']
                uri = s3_location['uri']
                
                # Extract the document name from the S3 URI
                document_name = os.path.basename(uri)
                
                # Create a unique identifier for this chunk
                chunk_id = f"{document_name}:{chunk_text[:50]}"  # Use first 50 chars of chunk as part of ID
                
                if chunk_id not in displayed_chunks:
                    with st.expander(f"Chunk {chunk_counter} - {document_name}"):
                        st.markdown(chunk_text)
                    chunk_counter += 1
                    displayed_chunks.add(chunk_id)

    st.session_state.messages.append({"role": "assistant", "content": answer})