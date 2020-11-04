from tasks import *

rr = [ add.apply_async((4,4), countdown=2), add.delay(4,5), hello.delay(), fail.delay(), slow.delay(2)]


assert add(4,4) == 8 # local run

for i, r in enumerate(rr):
    print(i,  r.get(propagate=False) , r.state, )



