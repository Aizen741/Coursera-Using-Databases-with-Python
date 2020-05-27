import sqlite3

x = sqlite3.connect('countdb.sqlite')
y = x.cursor()

y.execute('DROP TABLE IF EXISTS Counts')
y.execute('''CREATE TABLE Counts(org TEXT, count INTEGER)''')

file = 'mbox.txt'
open_file = open(file)

for line in open_file:

    if not line.startswith('From:'): continue

    words = line.split()
#-------------------------------------------------
# This split is used to split the emails froms '@'
    id = words[1]
    org =id.split('@')[1]
#--------------------------------------------------
    y.execute('SELECT count FROM Counts WHERE org =?', (org,))
    try:
        row = y.fetchone()[0]
        y.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (org,))

    except:
        y.execute('INSERT INTO Counts(org,count) VALUES(?,1)',(org,))

x.commit()
string_sql = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in y.execute(string_sql):
    print(row[0], row[1])
y.close()

