import streamlit as st
import pandas as pd
import os
from language_model import process_single_document
from process_Model import process_multiple_documents


def process_pdfs(folder_path, user_prompt, model_type):
    # Process PDFs and get results
    results = process_multiple_documents(folder_path, model_type, user_prompt)

    # Initialize lists to store file paths and results
    file_paths = []
    responses = []
    prompts = []

    # Iterate through results and gather file paths, responses, and prompts
    for pdf_file, result in results.items():
        file_paths.append(os.path.join(folder_path, pdf_file))
        responses.append(result)
        prompts.append(user_prompt)

    # Create DataFrame with results, file paths, and prompts
    res_df = pd.DataFrame({
        "file_path": file_paths,
        "response": responses,
        "prompt": prompts,
    })

    return res_df 




# Main Streamlit app code
def main():
    col1, col2, col3 = st.columns([1, 2, 5])

    with col1:
        st.image("/Users/admin/Documents/workspace/venv/Rag_Automation/RAG_prototype/VIRIDIEN_Logo.png", width=700)

    with col2:
        st.write("")  # Empty space to align with the title

    with col3:
        st.markdown("")

    st.title("PDF Processing Tool with Language Model")

    # Sidebar input for folder path and user prompt
    folder_path = st.text_input("Enter the folder path containing PDF files:")

    user_prompt = st.text_input("Enter prompt for language model:")

    # Dropdown for selecting model type
    model_type = st.selectbox("Select Model Type", ["llama3", "mistral"])

    file_name = st.text_input("Enter file name for saving results (without extension):", "results")

    # Process button
    if st.button("Process PDFs"):
        if folder_path:
            if os.path.isdir(folder_path):
                # Process PDFs and get results based on selected model type
                results_df = process_pdfs(folder_path, user_prompt, model_type)

                # Create a dedicated folder for saving results
                save_folder = "results"
                os.makedirs(save_folder, exist_ok=True)

                # Save results as CSV in the dedicated folder
                save_path = os.path.join(save_folder, f"{file_name}.csv")
                results_df.to_csv(save_path, index=False)

                # Display results
                st.success(f"Results saved successfully at {save_path}")
                st.dataframe(results_df)
            else:
                st.error(f"'{folder_path}' is not a valid directory.")
        else:
            st.warning("Please enter a folder path.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
