import os
import argparse
import ast
import openai
import nbformat
import configparser

CONFIG_FILE = os.path.expanduser("~/.py2notebook-ai")

def save_api_key(api_key):
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"OpenAI_API_Key": api_key}
    with open(CONFIG_FILE, "w") as f:
        config.write(f)
    print(f"API key saved successfully to {CONFIG_FILE}")

def load_api_key():
    if os.path.exists(CONFIG_FILE):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        return config["DEFAULT"].get("OpenAI_API_Key")
    else:
        return None

def parse_script(file_path):
    with open(file_path, 'r') as f:
        return ast.parse(f.read())

def generate_comment(code_block, api_key):
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert Python programmer who comments on code."},
                {"role": "user", "content": f"Comment on this Python code:\n{code_block}"}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error generating comment: {e}")
        return "Error generating comment."

def generate_title_and_description(script, api_key):
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert Python programmer who can generate titles and descriptions for scripts."},
                {"role": "user", "content": f"Generate a title and a description for the following Python script:\n{script}"}
            ]
        )
        title = response["choices"][0]["message"]["content"].strip().split("\n", 1)[0]  # Get the first line as title
        description = response["choices"][0]["message"]["content"].strip().split("\n", 1)[1]  # Get the rest as description
        return title, description
    except Exception as e:
        print(f"Error generating title and description: {e}")
        return "Error generating title", "Error generating description."

def create_notebook(title, description, blocks, comments):
    notebook = nbformat.v4.new_notebook()

    # Add the title and description as markdown cells at the top
    notebook.cells.append(nbformat.v4.new_markdown_cell(f"# {title}"))
    notebook.cells.append(nbformat.v4.new_markdown_cell(description))

    # Add the code blocks and comments
    for code, comment in zip(blocks, comments):
        notebook.cells.append(nbformat.v4.new_markdown_cell(comment))
        notebook.cells.append(nbformat.v4.new_code_cell(code))

    return notebook

def save_notebook(notebook, output_path):
    with open(output_path, 'w') as f:
        nbformat.write(notebook, f)

def main():
    parser = argparse.ArgumentParser(description="Convert Python script to Jupyter Notebook with AI comments.")
    subparsers = parser.add_subparsers(dest="command")

    # Command: convert
    convert_parser = subparsers.add_parser("convert", help="Convert a Python script to a Jupyter Notebook.")
    convert_parser.add_argument("script", help="Path to the Python script.")
    convert_parser.add_argument("-o", "--output", default="output.ipynb", help="Output notebook file.")
    convert_parser.add_argument("--api-key", help="OpenAI API key.")

    # Command: config set-key
    config_parser = subparsers.add_parser("config", help="Configure the tool.")
    config_subparsers = config_parser.add_subparsers(dest="config_command")
    set_key_parser = config_subparsers.add_parser("set-key", help="Set the OpenAI API key.")
    set_key_parser.add_argument("api_key", help="Your OpenAI API key.")

    args = parser.parse_args()

    if args.command == "config" and args.config_command == "set-key":
        save_api_key(args.api_key)
        return

    if args.command == "convert":
        api_key = args.api_key or load_api_key()
        if not api_key:
            print("Error: No API key provided. Use `py2notebook-ai config set-key` to save your API key.")
            return

        script = parse_script(args.script)
        code_blocks = [ast.unparse(node) for node in script.body if isinstance(node, ast.stmt)]
        comments = [generate_comment(block, api_key) for block in code_blocks]

        # Generate title and description for the notebook
        with open(args.script, 'r') as file:
            script_content = file.read()
        title, description = generate_title_and_description(script_content, api_key)

        # Create the notebook with title, description, and code blocks
        notebook = create_notebook(title, description, code_blocks, comments)
        save_notebook(notebook, args.output)
        print(f"Notebook saved to {args.output}")

