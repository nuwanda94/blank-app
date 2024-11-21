# File: crud_streamlit_app.py

import streamlit as st
import pandas as pd

# Initialize the app's session state for data storage
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "ID": [1, 2],
        "Name": ["Alice", "Bob"],
        "Age": [30, 25]
    })

# Helper functions
def get_next_id():
    """Generates the next unique ID for new entries."""
    if st.session_state.data.empty:
        return 1
    return st.session_state.data["ID"].max() + 1

def validate_name(name):
    """Validates that the name is non-empty and reasonable length."""
    if not name.strip():
        return "Name cannot be empty!"
    if len(name.strip()) > 50:
        return "Name is too long! Please keep it under 50 characters."
    return None

# App layout
st.title("Streamlit CRUD Interface")

# Tabs for each CRUD operation
tabs = st.tabs(["Create", "Read", "Update", "Delete"])

# Create
with tabs[0]:
    st.header("Create New Entry")
    
    # Form for input
    with st.form(key="create_form"):
        name = st.text_input("Name", key="name")
        age = st.number_input("Age", min_value=0, value=0, step=1, key="age")
        submitted = st.form_submit_button("Add Entry")

        if submitted:
            validation_error = validate_name(name)
            if validation_error:
                st.error(validation_error)
            else:
                new_entry = pd.DataFrame({
                    "ID": [get_next_id()],
                    "Name": [name.strip()],
                    "Age": [age]
                })
                st.session_state.data = pd.concat(
                    [st.session_state.data, new_entry], ignore_index=True
                )
                st.success("Entry added successfully!")

# Read
with tabs[1]:
    st.header("View Entries")
    if st.session_state.data.empty:
        st.info("No entries to display.")
    else:
        st.write("Current Data:")
        st.dataframe(st.session_state.data)

# Update
with tabs[2]:
    st.header("Update Entry")
    if st.session_state.data.empty:
        st.info("No entries available to update.")
    else:
        with st.form(key="update_form"):
            selected_id = st.selectbox(
                "Select ID to update",
                st.session_state.data["ID"],
                key="update_id"
            )
            entry_to_update = st.session_state.data[
                st.session_state.data["ID"] == selected_id
            ].iloc[0]

            updated_name = st.text_input("Updated Name", value=entry_to_update["Name"], key="updated_name")
            updated_age = st.number_input(
                "Updated Age", value=entry_to_update["Age"], min_value=0, step=1, key="updated_age"
            )
            update_submitted = st.form_submit_button("Update Entry")

            if update_submitted:
                validation_error = validate_name(updated_name)
                if validation_error:
                    st.error(validation_error)
                else:
                    st.session_state.data.loc[
                        st.session_state.data["ID"] == selected_id, ["Name", "Age"]
                    ] = [updated_name.strip(), updated_age]
                    st.success("Entry updated successfully!")

# Delete
with tabs[3]:
    st.header("Delete Entry")
    if st.session_state.data.empty:
        st.info("No entries available to delete.")
    else:
        with st.form(key="delete_form"):
            selected_id = st.selectbox(
                "Select ID to delete",
                st.session_state.data["ID"],
                key="delete_id"
            )
            delete_submitted = st.form_submit_button("Delete Entry")

            if delete_submitted:
                st.session_state.data = st.session_state.data[
                    st.session_state.data["ID"] != selected_id
                ]
                st.success("Entry deleted successfully!")
