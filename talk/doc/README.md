# dev-talk: python mental models


Foundations of programming and designing
with a Principle of Least Astonishment/Suprise allows you to learn and scale your development.


- install python in my system
- python is an interpreted language so let's launch interactive intepreter, write some instructions "in python-language" and hit enter to execute them
- complexity of my logic grows, I split my logic in a collection of functions: groups the code and present some sort of input/output/exceptions interface. Look
    ```python
    def add(x,y):
        if x<0:
            raise ValueError(f"Expected non-negative x, got {x=}")
        return x+y
    ```
    - inputs interface is "vaguely" defined as two "things" that are named as ``x,y``.
    - output interface is the sum of the inputs. The type will be resolved at runtime depending on the types of ``x`` and ``y`` and the result of the ``__add__`` operator on them
    - The function can also raise a ``ValueError`` exception. I like to account this as part of the interface.
- complexity of the logic grows and move all these functions inside a file ``mlib.py``. This creates a module that I can then use as a library.
```python
#!/local/bin/python3
def add(x,y):
    # same code as above
    ...

```
- So now in the python interpreter i can
```cmd
>> import mylib
>> mylib.add(3,4)
```
- This is still inconvenient since I have to open the interpreter, so let's transform our code in an executable, i.e. something like ``python`` itself that I can start directly from the terminal. An executable, analogously to a function, define an input/output/error interface. The interface we are interested for an executable is typically referred as a  command-line-interface (or CLI in short).
- The concept of CLI is a concept that exists since long, even before python. Other languages like C already create a way to programatically express the structure of a CLI, so why to reinvent the wheel?: python inherited most of the structure and most importantly some of the naming. 
> There are only two hard things in Computer Science: cache invalidation and naming things. 
> 
>-- Phil Karlton ([TwoHardThings])

- First let's use ``mlib`` as both library and executable script:
```python

#!/local/bin/python3
def add(x,y):
    # same code as above

import sys
import os

def main():
    program, x, y = sys.argv

    try:
        res = add(x,y)
        print(res, sys.stdout)
        return sys.exit(os.EX_OK)
    except ValueError as err:
        print(err, sys.stderr)
        raise
    

if __name__ == "__main__":
    main()
```
- now we can run directly from the command line without having to open the interpreter
```cmd
$ python mylib 3 4

```
## script (executable) vs module



## script (executable) vs module









[TwoHardThings]:https://martinfowler.com/bliki/TwoHardThings.html
[RealPython-main-functions]:https://realpython.com/python-main-function/