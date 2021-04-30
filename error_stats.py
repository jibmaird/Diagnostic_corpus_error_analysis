import re

f = open("errors_bert.manual2")

lines = f.readlines()
p0 = re.compile('\|(.*?\_....TIVE)\|')
p = re.compile('\* (.*)\n')
D = {}
for l in lines:

    m = p0.search(l)
    if m:
        k = m.group(1)
 
    m = p.match(l)
    if m:
        k = k + '_' + m.group(1)
        if k in D:
            D[k] = D[k]+1
        else:
            D[k] = 1
f.close()

for key, value in sorted(D.items(),
                         key=lambda item: item[1],reverse=True):
    print(key, ' :: ', value)

