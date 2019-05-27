import os
import sqlite3
from text_processor import get_words, process_word, process_text
import time

#------------------- INSERT QUERY HERE -------------------------------
query = "sistem spot"
#---------------------------------------------------------------------

results = {}
results_s = {}

def search_seq(query):
    file_index = 0
    for root, dirs, files in os.walk('../input/'):
         for file in files:
            if file.endswith("html"):
                with open(os.path.join(root, file), "r", encoding='utf8', errors='ignore') as f:
                    html = f.read()
                    word_list = process_text(html)
                    counter = 0
                    word_index = 0
                    index_list = []
                    for word in word_list:
                        word = process_word(word)
                        if word != "":
                            if word in query:
                                counter = counter + 1
                                index_list.append(word_index)
                        word_index = word_index + 1

                results_s[file_index] = [counter, file, index_list]
                file_index = file_index + 1

def get_results_s(sorted_results):
    # Find correct path
    for value in sorted_results:
        path = '../input/e-prostor.gov.si/' + value[1]
        if (not os.path.isfile(path)):
            path = '../input/e-uprava.gov.si/' + value[1]
            if (not os.path.isfile(path)):
                path = '../input/evem.gov.si/' + value[1]
                if (not os.path.isfile(path)):
                    path = '../input/podatki.gov.si/' + value[1]

        with open(path, "r", encoding='utf8', errors='ignore') as f:
            html = f.read()
            word_list = process_text(html)
            snippet = generate_snippet(word_list, value[2])
            print("%d\t\t\t %s\t\t\t\t\t%s" % (value[0], value[1], snippet))


def generate_snippet(word_list, indexes):
    snippet = ""
    for i in indexes:
        if len(snippet) > 200:
            snippet = snippet.replace("......", "...")
            return snippet
        if i+4 <= len(word_list):
            if i >= 3:
                snippet += "... " + " ".join(word_list[i - 3:i + 4]).replace(" ,", ",") + " ..."
            elif i == 2:
                snippet += "... " + " ".join(word_list[i - 2:i + 4]).replace(" ,", ",") + " ..."
            elif i == 1:
                snippet += "... " + " ".join(word_list[i - 1:i + 4]).replace(" ,", ",") + " ..."
            else:
                snippet += "".join(word_list[i:i + 3]) + "..."
        elif i+3 <= len(word_list):
            if i >= 3:
                snippet += "... " + " ".join(word_list[i - 3:i + 3]).replace(" ,", ",") + " ..."
            elif i == 2:
                snippet += "... " + " ".join(word_list[i - 2:i + 3]).replace(" ,", ",") + " ..."
            elif i == 1:
                snippet += "... " + " ".join(word_list[i - 1:i + 3]).replace(" ,", ",") + " ..."
            else:
                snippet += "".join(word_list[i:i + 3]) + "..."
        elif i+2 <= len(word_list):
            if i >= 3:
                snippet += "... " + " ".join(word_list[i - 3:i + 2]).replace(" ,", ",") + " ..."
            elif i == 2:
                snippet += "... " + " ".join(word_list[i - 2:i + 2]).replace(" ,", ",") + " ..."
            elif i == 1:
                snippet += "... " + " ".join(word_list[i - 1:i + 2]).replace(" ,", ",") + " ..."
            else:
                snippet += "".join(word_list[i:i + 3]) + "..."
        elif i+1 <= len(word_list):
            if i >= 3:
                snippet += "... " + " ".join(word_list[i - 3:i + 1]).replace(" ,", ",") + " ..."
            elif i == 2:
                snippet += "... " + " ".join(word_list[i - 2:i + 1]).replace(" ,", ",") + " ..."
            elif i == 1:
                snippet += "... " + " ".join(word_list[i - 1:i + 1]).replace(" ,", ",") + " ..."
            else:
                snippet += "".join(word_list[i:i + 3]) + "..."
        else:
            if i >= 3:
                snippet += "... " + " ".join(word_list[i - 3:i]).replace(" ,", ",") + " ..."
            elif i == 2:
                snippet += "... " + " ".join(word_list[i - 2:i]).replace(" ,", ",") + " ..."
            elif i == 1:
                snippet += "... " + " ".join(word_list[i - 1:i]).replace(" ,", ",") + " ..."
            else:
                snippet += "".join(word_list[i:i + 3]) + "..."
    snippet = snippet.replace("......", "...")
    return snippet


def get_results(query):
    conn = sqlite3.connect('../inverted-index.db')
    c = conn.cursor()
    sql = '''    
        SELECT p.documentName AS docName, SUM(frequency) AS freq, GROUP_CONCAT(indexes) AS idxs
        FROM Posting p
        WHERE
            p.word IN ({seq})
        GROUP BY p.documentName
        ORDER BY freq DESC;'''.format(seq=','.join(['?']*len(query)))
    cursor = c.execute(sql, query)
    for row in cursor:
        # Find correct path
        path ='../input/e-prostor.gov.si/'+row[0]
        if(not os.path.isfile(path)):
            path = '../input/e-uprava.gov.si/' + row[0]
            if (not os.path.isfile(path)):
                path = '../input/evem.gov.si/' + row[0]
                if (not os.path.isfile(path)):
                    path = '../input/podatki.gov.si/' + row[0]

        with open(path, "r", encoding='utf8', errors='ignore') as f:
            html = f.read()
            word_list = process_text(html)
            indexes = [int(s) for s in row[2].split(',')]
            snippet = generate_snippet(word_list, indexes)
            print("%d\t\t\t %s\t\t\t\t\t%s" % (row[1], row[0], snippet))


start_time = time.time()
print("Results for a query: \'" + query  +"\'")
query = query.split()
processed_query = []
for word in get_words(query):
    word = process_word(word)
    if word != "":
        processed_query.append(word)

#print("Cleaned query: " + str(processed_query))
print()
print("Frequencies Document                                  Snippet")
print("----------- ----------------------------------------- -----------------------------------------------------------")
get_results(processed_query)
print("\n\nResults found in %s seconds." % (time.time() - start_time))

start_time = time.time()
#print("Cleaned query: " + str(processed_query))
print()
print("Frequencies Document                                  Snippet")
print("----------- ----------------------------------------- -----------------------------------------------------------")
search_seq(processed_query)
sorted_results = sorted(results_s.values(), key=lambda kv: kv[0],reverse=True)
print(sorted_results)
get_results_s(sorted_results)
print("\n\nResults found in %s seconds." % (time.time() - start_time))

'''
def get_doc(word):
    conn = sqlite3.connect('../inverted-index.db')
    c = conn.cursor()
    sql = "SELECT * FROM Posting WHERE word = ? ORDER BY frequency desc"
    c.execute(sql, (word,))
    rows = c.fetchall()
    conn.commit()
    conn.close()
    return rows


results = {}
for word in query:
   rows = get_doc(word)
   for row in rows:
        if row[1] in results:
           freq = row[2]
           results[row[1]][0] += freq
           results[row[1]][1].append(row)
        else:
           freq = row[2]
           results[row[1]] = [freq,[row]]

sorted_results = sorted(results.values(), key=lambda kv: kv[0],reverse=True)

for  data in sorted_results:
   print(data)


'''
