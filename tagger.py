import os
import shutil

import openai


def add_tags_to_md(source_content, tags_str):
    """
    Adds or updates the 'tags' metadata in a Markdown note.
    
    Parameters:
    - source_content (str): The original content of the note.
    - tags_str (str): A comma-separated string of new tags to add.
    
    Returns:
    - str: The note content with updated 'tags' metadata.
    """
    # Extract existing metadata and content
    if source_content.strip().startswith('---'):
        parts = source_content.split('---', 2)
        metadata_str = parts[1].strip()
        content = parts[2].strip() if len(parts) > 2 else ""
    else:
        metadata_str, content = "", source_content.strip()
    
    # Extract existing tags
    existing_tags = []
    new_metadata_lines = []
    for line in metadata_str.split("\n"):
        if line.startswith("tags:"):
            existing_tags.extend(line.replace("tags:", "").strip().split(", "))
        else:
            new_metadata_lines.append(line)

    # Return the original content if there are existing tags
    if existing_tags:
        return source_content.strip()
    
    # Combine existing and new tags, removing duplicates
    new_tags = tags_str.split(", ")
    combined_tags = list(set(new_tags))
    
    # Reassemble metadata
    if combined_tags:
        new_metadata_lines.append(f"tags: {', '.join(combined_tags)}")
    new_metadata_str = "\n".join(new_metadata_lines)
    
    # Ensure the metadata is enclosed in ---
    return f"---\n{new_metadata_str}\n---\n{content}".strip()

def auto_tagging(api_key):
    """
    Automatically adds tags to all Markdown files in the current directory using OpenAI's API and organizes them into relevant folders.
    
    Parameters:
    - api_key (str): The OpenAI API key.
    - sensitive_words (list): A list of words to check for skipping files.
    """
    # Set OpenAI API key
    openai.api_key = api_key

    # Initialize lists to keep track of processed and skipped files
    processed, skipped = [], []

    # Loop through all Markdown files in the directory
    for index, filename in enumerate(os.listdir(".")):
        if filename.endswith(".md"):
            # Read file content
            with open(filename, 'r', encoding='utf-8') as f:
                source_content = f.read()

            # Check if the file already has tags
            if "---" in source_content:
                parts = source_content.split('---', 2)
                metadata_str = parts[1].strip()
                if any(line.startswith("tags:") for line in metadata_str.split("\n")):
                    skipped.append(filename)
                    continue

            # Fetch tags from OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that formats tags for Obsidian notes."},
                    {"role": "user", "content": f"Extract keywords for tags from the following content. In case the text is short please try to infer the meaning. When tagging abbreviations also add the word as a tag. Format them as a comma-separated list:\n\n{source_content}"}
                ]
            )
            tags_str = response.choices[0].message['content'].strip()

            # Update note with new tags
            new_content = add_tags_to_md(source_content, tags_str)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)

            processed.append(filename)
            print(f"PROGRESS: {index / len(os.listdir('.')):.2%}")

    # Rewrite titles
    #rewrite_title(api_key,processed)
    # Organize processed files into folders
    organize_files(api_key, processed)


def organize_files(api_key, processed_files):
    """
    Organizes the processed files into relevant folders based on GPT's reasoning.

    Parameters:
    - api_key (str): The OpenAI API key.
    - processed_files (list): List of processed files.
    """
    existing_folders = [d for d in os.listdir() if os.path.isdir(d)]
    
    for filename in processed_files:
        # Query GPT for the appropriate folder
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that organizes files into relevant folders."},
                {"role": "user", "content": f"Here is a list of existing folders: {existing_folders}. Suggest a relevant folder to place the following file. Provide the folder name in the format [[folder_name]]. Avoid creating too many new folders and use subfolders when appropriate.\n\nFilename: {filename}"}
            ]
        )
        folder_response = response.choices[0].message['content'].strip()
        
        # Extract folder name
        folder_name = folder_response.split("[[")[1].split("]]")[0]
        
        # Ensure the folder exists
        if folder_name not in existing_folders:
            os.makedirs(folder_name, exist_ok=True)
            existing_folders.append(folder_name)
        
        # Move the file to the appropriate folder
        shutil.move(filename, os.path.join(folder_name, filename))
        print(f"Moved {filename} to {folder_name}")

# Run the script
auto_tagging("YOUR_API_KEY_HERE")
