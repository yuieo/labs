#вариант 1

print('задание 1')
import itertools
k = 0
a = list(itertools.product('ТИМОФЕЙ', repeat=5))
for x in a:
    if x.count('Й') == 1 and x[0]!='Й' and x[4]!='Й' and x.count('ЙИ')==0 and x.count('ИЙ')==0:
        k+=1

print(k)


print('\nзадание 2')
result = 4**2020 + 2**2017 - 15
bin_result = bin(result)
print(bin_result.count('1'))


print('\nзадание 3')
for n in range(174457, 174505 + 1):
    segment = []
    for d in range(2, n//2 + 1):
        if n % d == 0:
            segment.append(d)
            if len(segment) > 2:
                break
    if len(segment) == 2:
        print(segment[0], segment[1])