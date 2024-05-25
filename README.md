# Obsidian-PKM AutoTagger

This Python script designed to automatically add tags to all markdown files in the current Obsidian directory, utilizing OpenAI:s gpt4-o. It also organizes these files into relevant folders based on their content.
The goal was to create a super simple and lean MVP approach to easing my PKM workflow, and expanding with more features and complexity later on.

## Features

- **Automatic Tagging**: Adds tags to Markdown files based on their content.
- **Content-Based Organization**: Organizes processed files into appropriate folders.
- **Duplicate Avoidance**: Skips files that already have tags.
- **Metadata Management**: Ensures metadata is properly enclosed in `---` in the Markdown files.

## Requirements

- Python 3.6+
- `openai` Python library
- OpenAI API key

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/danielofosu/Obsidian-PKM.git
    cd Obisidan-PKM
    ```

2. Install the required Python packages:

    ```sh
    pip install openai
    ```
3. Replace the API key placeholder with your own OpenAI API key in the auto_tagging function call.

## Manual Usage

1. Ensure your OpenAI API key is available, and properly set up. Preferably with spending limits e.g. 5 euros per month.
2. Place the script in your Obsidian main directory.
3. Run the script:

    ```sh
    python3 tagger.py
    ```

## Running with Mac Automator

You can set up this script to run using Mac Automator for convenience, instead of running it manually.

### Step-by-Step Guide

1. **Open Automator**:
    - Open the Automator application on your Mac.

2. **Create a New Workflow**:
    - Choose "Workflow" when prompted to select a document type.

3. **Add "Run Shell Script" Action**:
    - In the search bar on the left, type "Run Shell Script".
    - Drag the "Run Shell Script" action into the workflow area.

4. **Configure the Shell Script**:
    - Set the "Shell" to `/bin/bash`.
    - Set the "Pass input" option to `as arguments`.
    - Replace the default script with the following, modifying the path to your `tagger.py` script:

      ```sh
      cd /path/to/script
      python3 tagger.py
      ```

5. **Save the Workflow**:
    - Save the workflow with a name like "Run Tagger".

6. **Run the Workflow**:
    - You can now run this workflow directly from Automator, or you can set it up to run at specific times using the Calendar app or other scheduling tools.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Utilizes Obsidian as the front-end for accessing the notes.
- Utilizes OpenAI's gpt-4o API for intelligent tagging and organization.

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) for more details.
