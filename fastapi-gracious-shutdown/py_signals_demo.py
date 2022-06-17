#
#
# https://medium.com/fintechexplained/advanced-python-how-to-use-signal-driven-programming-in-applications-84fcb722a369
#
#

import signal
import sys
import time


def my_custom_handler(signum, stack_frame):
   print('I have encountered the signal KILL.')
   print('CTRL+C was pressed.  Do anything here before the process exists')
   sys.exit(0)


def my_handler(signum, frame):
 print("Took too long")
 raise TimeoutError("took too long")



# SIGINT signal is raised by the operating system whenever CTRL + C is pressed to kill a process in Unix. It is essentially the KeyboardInterrupt exception
# signal.signal(signal.SIGINT, my_custom_handler) # By default signal.SIGINT tranlsates to KeyboardInterrupt exception
signal.signal(signal.SIGALRM, my_handler)
signal.alarm(10)


def get_data():
 time.sleep(20)

if __name__ == "__main__":
   get_data()
   # - The signals are always executed in the main Python thread.
   # - inter-thread communication then use the synchronisation primitives from the threading module


