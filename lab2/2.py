#вариант 1
#задание 1

import itertools
k = 0
a = list(itertools.product('ТИМОФЕЙ', repeat=5))
for x in a:
    if x.count('Й') == 1 and x[0]!='Й' and x[4]!='Й' and x.count('ЙИ')==0 and x.count('ИЙ')==0:
        k+=1

print(k)