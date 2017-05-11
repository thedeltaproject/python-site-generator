import re

string = '''---
twitter:card=dickbutt
twitter:title=dickbutt
twitter:description=dickbutt
twitter:image=dickbutt
---
<p>test</p>'''

pattern = '---\n(.+=.+\n)+---\n'
dictionary = {}

match = re.match(pattern, string)
if match:
    entries = re.split("\n", match.group(0)[4:-4])
    if entries[-1] == '':
        entries.pop()
    for i in range(len(entries)):
        entry = re.split("=", entries[i])
        dictionary[entry[0]] = entry[1]
    print(dictionary)
