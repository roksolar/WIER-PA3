import os

def indexer():
    html_list = []
    for root, dirs, files in os.walk('../input'):
         for file in files:
            with open(os.path.join(root, file), "r", encoding='utf8', errors='ignore') as f:
                file_contents = f.read()
                html_list.append(file_contents)
    return html_list
