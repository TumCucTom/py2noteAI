# Py2Notebook AI

Py2Notebook AI is a Python library that transforms Python scripts into Jupyter Notebooks. The tool leverages AI to generate insightful comments for each code block, helping to document and explain the code effectively.

## Features
- Converts Python scripts into Jupyter Notebook format.
- AI-generated comments for code blocks to improve understanding.
- Easy-to-use command-line interface.
- Supports customization for code block explanations.

## Installation
Install Py2Notebook AI via pip:
```bash
pip install py2notebook-ai
```

## Usage
To convert a Python script to a Jupyter Notebook with AI-generated comments:
```bash
py2notebook-ai convert your_script.py -o output_notebook.ipynb
```

### Example
Input: `your_script.py`
```python
# your_script.py
def add(a, b):
    return a + b

result = add(5, 3)
print(result)
```

Output: `output_notebook.ipynb`
- A Jupyter Notebook with the code, comments explaining the `add` function, and the printed result.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to enhance the functionality or fix bugs.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

