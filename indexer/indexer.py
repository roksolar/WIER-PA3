import os
import sqlite3

def indexer():
    html_list = []
    for root, dirs, files in os.walk('../input'):
         for file in files:
            with open(os.path.join(root, file), "r", encoding='utf8', errors='ignore') as f:
                file_contents = f.read()
                html_list.append(file_contents)
    return html_list


def write_to_index_word(word):
    conn = sqlite3.connect('../inverted-index.db')
    c = conn.cursor()
    sql = "INSERT INTO IndexWord VALUES (?)"
    c.execute(sql, (word,))
    conn.commit()
    conn.close()

def write_to_index_posting(word, document, frequency, index):
    conn = sqlite3.connect('../inverted-index.db')
    c = conn.cursor()
    sql = "INSERT INTO Posting VALUES  (?,?,?,?)"
    c.execute(sql, (word, document, frequency, index,))
    conn.commit()
    conn.close()



