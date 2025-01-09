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

def generate_comment(code, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Explain this Python code."},
            {"role": "user", "content": code},
        ],
    )
    return response["choices"][0]["message"]["content"]

def create_notebook(blocks, comments):
    notebook = nbformat.v4.new_notebook()
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

        notebook = create_notebook(code_blocks, comments)
        save_notebook(notebook, args.output)
        print(f"Notebook saved to {args.output}")
