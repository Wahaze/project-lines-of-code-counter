# project-lines-of-code-counter
This Python script recursively scans a project directory, ignoring folders like node_modules. It aggregates all text files into a single .txt file and generates a rich HTML report with overall project stats including total number of lines of code, a file size leaderboard, and the full content of each file for easy analysis and archiving.

This script is a powerful utility for developers, writers, and project managers who need to consolidate and analyze the contents of a text-based project. It recursively scans a specified directory, intelligently detects text files, and generates two distinct outputs: a single plain text file containing the content of all files, and a sophisticated, modern HTML report for in-depth analysis.

## Features

-   **Recursive Directory Scanning**: Traverses an entire project directory to find all relevant files.
-   **Intelligent Text File Detection**: Uses the `chardet` library to accurately identify text files and their encoding, avoiding binary files.
-   **Smart Exclusions**: Automatically ignores common development folders like `node_modules`, `dist`, and `dist-electron`, as well as files like `package-lock.json`, to keep the output clean.
-   **Dual File Output**: Generates both a `.txt` and an `.html` file.
    -   **`contenu_{project_name}.txt`**: A straightforward concatenation of all found text files, perfect for quick searches or AI model ingestion.
    -   **`analyse_{project_name}.html`**: A rich, interactive, single-page HTML report.
-   **In-Depth HTML Report**: The generated HTML file includes:
    -   A dynamic header with the project name and generation date.
    -   A dashboard of key statistics: total number of files, characters, words, and lines.
    -   A comprehensive table of all analyzed files, ranked by character count.
    -   Color-coded badges for different file extensions for easy identification.
    -   A detailed view of the full content of each file.
    -   A clean, responsive design for easy viewing on any device.
    -   A "Scroll to Top" button for easy navigation.

## Requirements

-   Python 3.x
-   The `chardet` library

## Installation

1.  **Clone the repository or save the script:**
    Save the code as `enhanced-consolidation-script.py`.

2.  **Install the required dependency:**
    Open your terminal or command prompt and run:
    ```sh
    pip install chardet
    ```

## How to Use

Run the script from your terminal, passing the path to the directory you want to analyze as an argument.

**Syntax:**
```sh
python enhanced-consolidation-script.py /path/to/your/project

Example:
If you have a project located at ~/documents/my-cool-app, you would run:
python enhanced-consolidation-script.py ~/documents/my-cool-app

The script will print the progress to the console as it analyzes each file.
Output
After the script finishes, two new files will be created in the directory where you ran the script:
contenu_my-cool-app.txt: A plain text file containing the content of all your project's text files, separated by headers.
analyse_my-cool-app.html: A detailed HTML report. Open this file in your web browser to view the project analysis.
The {project_name} in the filenames is automatically derived from the name of the directory you provided.
Customization
You can customize the script by editing the list of excluded directories or files. Open the .py file and modify the dossiers_exclus list within the doit_ignorer_chemin and parcourir_repertoire functions to add or remove paths to ignore.
# In the doit_ignorer_chemin and parcourir_repertoire functions...
dossiers_exclus = ['node_modules', 'dist', 'dist-electron', '.git', '__pycache__'] # Add your folders here

License
This project is open-source and available under the MIT License.
