import re

f = open("errors_bert.manual")
fo = open("errors_bert.manual2", "w")

lines = f.readlines()
p = re.compile('.*\|Characteristic')
for l in lines:
    fo.write(l)
    if p.search(l):
        fo.write('* \n')

f.close()
fo.close()
