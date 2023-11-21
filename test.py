from os import walk, getcwd, listdir, path

a = getcwd()
print(a)
b = path.dirname(a)
print(b)
c = path.dirname(b)
print(c)
d = path.dirname(c)
print(d)
e = path.dirname(d)
print(e)
