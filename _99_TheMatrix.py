import random
import time

rand = random.Random()
r = rand.randrange
alist = []
Sa = 0
blist = []
Sb = 0
list_tuple_ab = []
for n in range(0, 31):
    Sa += 10 ** n
    alist.append(Sa)
alist.reverse()

for n in range(0, 31):
    Sb += 9*10 ** n
    blist.append(Sb)
blist.reverse()

for i in range(31):
    list_tuple_ab.append((alist[random.randrange(1,31)],blist[random.randrange(1,31)]))

a = alist[random.randrange(1,31)]
b = blist[random.randrange(1,31)]
c = alist[random.randrange(1,31)]
d = blist[random.randrange(1,31)]
e = alist[random.randrange(1,31)]
f = blist[random.randrange(1,31)]
g = alist[random.randrange(1,31)]
h = blist[random.randrange(1,31)]
i = alist[random.randrange(1,31)]
j = blist[random.randrange(1,31)]


def changechar(my_string,char,number):
    l = list(my_string)
    char = " "
    number = len(l)-1


def compareinf(a, b):
    if a < b:
        return a
    else:
        return b


def comparesup(a, b):
    if a > b:
        return a
    else:
        return b

randomlist = [r(compareinf(a, b), comparesup(a, b)), r(compareinf(c, d), comparesup(c, d)), r(compareinf(e,f),comparesup(e, f)), r(compareinf(g, h),comparesup(g,h)), r(compareinf(i,j),comparesup(i,j))]

for i in range(100):
    print(randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)])
    time.sleep(0.02)
for i in range(100):
    print(randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)])
    time.sleep(0.02)
for i in range(100):
    print(randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)])
    time.sleep(0.02)
for i in range(100):
    print(randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)])
    time.sleep(0.02)
for i in range(100):
    print(randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)])
    time.sleep(0.02)
for i in range(100):
    print(randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)])
    time.sleep(0.02)
for i in range(100):
    print(randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)])
    time.sleep(0.02)
for i in range(100):
    print(randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)])
    time.sleep(0.02)
for i in range(100):
    print(randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)])
    time.sleep(0.02)
for i in range(100):
    print(randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)])
    time.sleep(0.02)
for i in range(100):
    print(randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)])
    time.sleep(0.02)
for i in range(100):
    print(randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)],randomlist[r(1,5)])
    time.sleep(0.02)