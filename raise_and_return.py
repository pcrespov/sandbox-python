from asyncio import CancelledError

def fail():
    raise CancelledError("failed")

def go():
    try:
        fail()
    except CancelledError as err:
        resp = 42
        raise
    finally:
        resp+=1
        return resp

try:
    resp = go()
finally:
    print(resp)
