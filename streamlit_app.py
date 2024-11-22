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

# Create Tab
with tabs[0]:
    st.header("Create New Entries")

    # Step 1: User specifies the number of records
    num_records = st.number_input("How many records do you want to add?", min_value=1, step=1, key="num_records")

    # Step 2: Dynamically generate inputs for the specified number of records
    if num_records:
        with st.form(key="multi_create_form"):
            new_data = []
            for i in range(int(num_records)):
                st.write(f"### Record {i + 1}")
                name = st.text_input(f"Name for Record {i + 1}", key=f"name_{i}")
                age = st.number_input(f"Age for Record {i + 1}", min_value=0, step=1, key=f"age_{i}")
                new_data.append({"Name": name, "Age": age})
            
            # Step 3: Submit button for previewing entries
            preview_submit = st.form_submit_button("Preview Entries")

            if preview_submit:
                # Prepare the data for preview
                preview_data = pd.DataFrame(new_data)
                st.write("### Editable Preview")

                # Editable inputs for previewed data
                edited_data = []
                for idx, row in preview_data.iterrows():
                    st.write(f"### Edit Record {idx + 1}")
                    edit_name = st.text_input(f"Edit Name for Record {idx + 1}", value=row["Name"], key=f"edit_name_{idx}")
                    edit_age = st.number_input(f"Edit Age for Record {idx + 1}", value=row["Age"], min_value=0, step=1, key=f"edit_age_{idx}")
                    edited_data.append({"Name": edit_name, "Age": edit_age})

                # Step 4: Validate edited data and add to the dataset
                if st.button("Confirm and Add Records"):
                    errors = []
                    valid_entries = []
                    for i, entry in enumerate(edited_data):
                        validation_error = validate_name(entry["Name"])
                        if validation_error:
                            errors.append(f"Record {i + 1}: {validation_error}")
                        else:
                            valid_entries.append({
                                "ID": get_next_id() + len(valid_entries),  # Increment IDs for each valid entry
                                "Name": entry["Name"].strip(),
                                "Age": entry["Age"]
                            })

                    if errors:
                        st.error("Some records have errors. Please fix them:")
                        for error in errors:
                            st.error(error)
                    else:
                        # Add valid entries to the dataset
                        new_entries_df = pd.DataFrame(valid_entries)
                        st.session_state.data = pd.concat(
                            [st.session_state.data, new_entries_df], ignore_index=True
                        )
                        st.success(f"Successfully added {len(valid_entries)} records!")
                        st.experimental_rerun()  # Refresh to clear inputs after adding

# Read Tab
with tabs[1]:
    st.header("View Entries")
    if st.session_state.data.empty:
        st.info("No entries to display.")
    else:
        st.write("Current Data:")
        st.dataframe(st.session_state.data)

# Update Tab
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

# Delete Tab
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
