import matplotlib.pyplot as plt
import sqlite3
from collections import Counter
import numpy as np

conn = sqlite3.connect('death_row.sqlite')
cur = conn.cursor()

graph_array = []
for row in cur.execute('''SELECT county FROM inmates'''):
    startingInfo = str(row).replace(')', '').replace('(', '').replace('u\'', '').replace("'", "")
    splitInfo = startingInfo.replace(',', '')
    graph_array.append(splitInfo)

print("graph_array:", graph_array)

counts = Counter(graph_array)
print("counts:", counts)

common = counts.most_common()
print("common:", common)

labels = [item[0] for item in common]
print("labels:", labels)

number = [item[1] for item in common]
print("numbers:", number)

nbars = len(common)
print("nbars:", nbars)

plt.figure(figsize=(19, 10))
plt.bar(np.arange(nbars), number, tick_label=labels)
plt.title("Number Of Death Sentences By County")
plt.ylabel("Number Of Death Sentences")
plt.xticks(rotation='vertical')
plt.show()

