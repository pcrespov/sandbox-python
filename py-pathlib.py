import os
from pathlib import Path




def check_relative_paths():
    # 
    # https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.relative_to
    # difference between p.relative_to and os.path.relpath

    p = Path("/etc/password")
    print(f"{p.relative_to('/etc')=}")
    print( f"{os.path.relpath(p,'/etc')=}" )


    # but what if it has a different start?
    q = Path("/usr")
    try:
        q.relative_to(p)
    except ValueError as err:
        print(f"{err=}")
    print( f"{os.path.relpath(q,p)=}" )



if __name__ == "__main__":
    check_relative_paths()