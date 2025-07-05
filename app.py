import streamlit as st
import uuid
import os
import json

# Folder to store text snippets
STORAGE_DIR = "snippets"
os.makedirs(STORAGE_DIR, exist_ok=True)

st.set_page_config(page_title="KuickText", page_icon="📝")
st.title("📝 KuickText: Instant Text Sharing")

menu = st.sidebar.radio("Choose an option", ["Paste Text", "View Snippet"])

if menu == "Paste Text":
    user_text = st.text_area("Paste your text below:")

    if st.button("Generate Shareable Link"):
        if not user_text.strip():
            st.warning("Please enter some text to share.")
        else:
            unique_id = str(uuid.uuid4())[:8]
            with open(f"{STORAGE_DIR}/{unique_id}.json", "w") as f:
                json.dump({"text": user_text}, f)

            # Use your Streamlit Cloud URL
            base_url = "https://share-text-by-chethu.streamlit.app"
            share_url = f"{base_url}/?id={unique_id}"

            st.success("✅ Shareable Link Generated!")
            st.code(share_url)
            st.markdown(f"[Click to view]({share_url})")

elif menu == "View Snippet":
    query_params = st.query_params
    query_id = query_params.get("id", [None])[0]

    if query_id:
        file_path = f"{STORAGE_DIR}/{query_id}.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
                st.subheader("📄 Shared Text:")
                st.text_area("Your Snippet", value=data["text"], height=300)
        else:
            st.error("❌ Snippet not found or expired.")
    else:
        st.info("🔗 Provide a snippet ID in the URL to view a shared snippet.")
