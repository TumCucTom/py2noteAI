import argparse
from py2notebook_ai.main import parse_script, create_notebook, save_notebook, generate_comment, save_api_key, load_api_key
import ast

def convert_command(args):
    # Load API key or use the one provided via CLI
    api_key = args.api_key or load_api_key()
    if not api_key:
        print("Error: No API key provided. Use `py2notebook-ai config set-key` to save your API key.")
        return

    # Parse the script
    script = parse_script(args.script)
    code_blocks = [ast.unparse(node) for node in script.body if isinstance(node, ast.stmt)]

    comments = []
    for block in code_blocks:
        try:
            comment = generate_comment(block, api_key)
            comments.append(comment)
        except Exception as e:
            print(f"Error generating comment for block: {e}")
            comments.append("Error generating comment.")

    # Create and save the notebook
    notebook = create_notebook(code_blocks, comments)
    save_notebook(notebook, args.output)
    print(f"Notebook saved to {args.output}")

def config_command(args):
    if args.config_command == "set-key":
        save_api_key(args.api_key)

def main():
    parser = argparse.ArgumentParser(description="Convert Python scripts into Jupyter Notebooks with AI-generated comments.")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: convert
    convert_parser = subparsers.add_parser("convert", help="Convert a Python script to a Jupyter Notebook.")
    convert_parser.add_argument("script", help="Path to the Python script.")
    convert_parser.add_argument("-o", "--output", default="output.ipynb", help="Output notebook file.")
    convert_parser.add_argument("--api-key", help="OpenAI API key.")

    # Subcommand: config
    config_parser = subparsers.add_parser("config", help="Configure the tool.")
    config_subparsers = config_parser.add_subparsers(dest="config_command")
    set_key_parser = config_subparsers.add_parser("set-key", help="Set the OpenAI API key.")
    set_key_parser.add_argument("api_key", help="Your OpenAI API key.")

    args = parser.parse_args()

    if args.command == "convert":
        convert_command(args)
    elif args.command == "config":
        config_command(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
