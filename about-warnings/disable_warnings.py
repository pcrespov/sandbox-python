## https://stackoverflow.com/questions/14463277/how-to-disable-python-warnings

import warnings

#with warnings.catch_warnings():

def fxn():
    print('fxn')
    warnings.warn("deprecated fxn", FutureWarning)

def gx():
    print('gx')
    warnings.warn("deprecated gx", FutureWarning)

#fxn()

# fxn()


# with warnings.catch_warnings():
#     #warnings.simplefilter("ignore")
#     warnings.filterwarnings("ignore", message="deprecated fxn") 
#     gx()
#     fxn()