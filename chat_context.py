import ollama
import streamlit as st

st.title("PyOpenChat: The chatbot using Open LLMs")

## Initialising the chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

## Initialising models
if "model" not in st.session_state:
    st.session_state["model"] = ""

## To select a LLM models from a list of available models
models = [model["name"] for model in ollama.list()["models"]]
st.session_state["model"] = st.selectbox("Please Select Your Model", models)

## Generator funtion to show the generated result of LLMs
def model_result_generator():
    stream = ollama.chat(
        model=st.session_state["model"],
        messages=st.session_state["messages"],
        stream=True,
    )
    for chunk in stream:
        yield chunk["message"]["content"]

## Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

## Input for the promt
if prompt := st.chat_input("At Your Service, My Lord?"):

    # add latest message to history in format {role, content}
    st.session_state["messages"].append({"role": "user", "content": prompt})
    
    # Show the chat history on the page
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking ..."):
            message = st.write_stream(model_result_generator())
            st.session_state["messages"].append({"role": "assistant", "content": message})
