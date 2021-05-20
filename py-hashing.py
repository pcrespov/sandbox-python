import pickle

x = {"x": 1, "y": 2}
xs = {"y": 2, "x":1}
msg = "foo"
value = 34.5


assert hash(msg) == hash(msg)
# Every run will produce different hash values!
print(hash(msg))
print(hash(value))
#print(hash(frozenset(x.items())))

#print(x)
#print(xs)

# frozenset 
#print(frozenset(x.items()))
#print(frozenset(xs.items()))

# but every run will be a different order!
assert frozenset(x.items()) == frozenset(xs.items())