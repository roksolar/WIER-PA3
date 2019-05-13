import sqlite3
from text_processor import get_words

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
        print("\tHits: %d\n\t\tDoc: '%s'\n\t\tIndexes: %s" % (row[1], row[0], row[2]))

query = ['test.,','in', 'spot']
print(query)
query = get_words(query)
print(query)
get_results(['test','spot'])


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
