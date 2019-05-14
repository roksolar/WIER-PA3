import os
import sqlite3
from text_processor import process_text, process_word


def indexer():
    # Read all HTML files in input folder
    for root, dirs, files in os.walk('../input'):
         for file in files:
            if file.endswith("html"):
                with open(os.path.join(root, file), "r", encoding='utf8', errors='ignore') as f:
                    print(file)
                    html = f.read()
                    word_list = process_text(html)
                    unique_word_list = []
                    for word in word_list:
                        word = process_word(word)
                        if word != "":
                            try:
                                write_to_index_word(word)
                            except Exception as e:
                                pass
                            if word not in unique_word_list:
                                generate_posting(word, word_list, file)
                                unique_word_list.append(word)


def generate_posting(word,word_list, file):
    index = []
    count_frequency = 0
    for i, element in enumerate(word_list):
        element = process_word(element)
        if element == word:
            index.append(i)
            count_frequency += 1
    try:
        write_to_index_posting(word, file, count_frequency, str(index)[1:len(str(index))-1])
    except Exception as e:
        pass


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


indexer()
