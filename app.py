import streamlit as st
import uuid
import os
import json

STORAGE_DIR = "snippets"
os.makedirs(STORAGE_DIR, exist_ok=True)

st.title("KuickText: Instant Text Sharing")

menu = st.sidebar.radio("Choose an option", ["Paste Text", "View Snippet"])

if menu == "Paste Text":
    user_text = st.text_area("Paste your text below:")
    if st.button("Generate Shareable Link"):
        unique_id = str(uuid.uuid4())[:8]
        with open(f"{STORAGE_DIR}/{unique_id}.json", "w") as f:
            json.dump({"text": user_text}, f)

        share_url = f"https://share-text-by-chethu.streamlit.app/?id={unique_id}"
        st.success("Link Generated!")
        st.code(share_url)

elif menu == "View Snippet":
    query_params = st.experimental_get_query_params()
    query_id = query_params.get("id", [None])[0]
    if query_id:
        try:
            with open(f"{STORAGE_DIR}/{query_id}.json", "r") as f:
                data = json.load(f)
                st.text_area("Shared Text", value=data["text"], height=300)
        except FileNotFoundError:
            st.error("Snippet not found or expired.")
    else:
        st.info("No snippet ID provided in URL.")
