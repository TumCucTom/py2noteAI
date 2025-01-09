from py2notebook_ai.main import parse_script, create_notebook

def test_parse_script():
    code = "def hello():\n    print('Hello, world!')"
    script = parse_script("example.py")
    assert script.body[0].name == "hello"

def test_create_notebook():
    blocks = ["print('Hello')"]
    comments = ["This prints Hello."]
    notebook = create_notebook(blocks, comments)
    assert len(notebook.cells) == 2
