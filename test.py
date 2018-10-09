listT = []
for i in range(10):
    listT.append(i)
print(listT)

iterator = iter(listT)
a = listT[0]
while a < 5: 
    a = next(iterator)
    print(a)

print("out")
while a < 10:
    a = iterator.next()
    print(a)