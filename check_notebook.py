import json
with open('notebooks/economic_analysis.ipynb', 'r') as f:
    nb = json.load(f)
print([cell['cell_type'] for cell in nb['cells']])