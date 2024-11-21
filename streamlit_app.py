import streamlit as st
import pandas as pd

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
# Upload Excel File
uploaded_file = st.file_uploader("Upload an Excel file (single sheet)", type=["xlsx", "xls"])

if uploaded_file:
    try:
        # Read Excel File
        df = pd.read_excel(uploaded_file)
        st.write("**Preview of Uploaded Data:**")
        st.dataframe(df.head())

        # Remove Duplicates
        if st.checkbox("Remove duplicate rows"):
            df = df.drop_duplicates()
            st.write("**Duplicates removed. Updated Data:**")
            st.dataframe(df.head())
    except Exception as e:
        st.error(f"An error occurred: {e}")
