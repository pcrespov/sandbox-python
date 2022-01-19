

def fun(x,*, max_iterations=100):
    for _ in range(max_iterations):
        y = x + 1 
        x = yield y
