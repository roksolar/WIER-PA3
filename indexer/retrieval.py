import sqlite3

def get_doc(word):
    conn = sqlite3.connect('../inverted-index.db')
    c = conn.cursor()
    sql = "SELECT * FROM Posting WHERE word = ? ORDER BY frequency desc"
    c.execute(sql, (word,))
    rows = c.fetchall()
    conn.commit()
    conn.close()
    return rows

query = ["sistem","spot"]
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


