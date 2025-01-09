import ast
import openai
import nbformat

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
    import argparse

    parser = argparse.ArgumentParser(description="Convert Python script to Jupyter Notebook with AI comments.")
    parser.add_argument("script", help="Path to the Python script.")
    parser.add_argument("-o", "--output", default="output.ipynb", help="Output notebook file.")
    parser.add_argument("--api-key", required=True, help="OpenAI API key.")

    args = parser.parse_args()

    script = parse_script(args.script)
    code_blocks = [ast.unparse(node) for node in script.body if isinstance(node, ast.stmt)]
    comments = [generate_comment(block, args.api_key) for block in code_blocks]

    notebook = create_notebook(code_blocks, comments)
    save_notebook(notebook, args.output)

if __name__ == "__main__":
    main()
