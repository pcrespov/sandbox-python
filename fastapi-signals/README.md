

> How a service can gracefully shutdown when there is a signal that restarts/update/stops/kills the container?

By "graceful shutdown" we mean how an app handles the start/stop event (e.g. due to kill signals, rolling updates, etc) to help avoiding
- data loss
- resource leaks (memory, connections, ...)
- requests loss
 


 CTRL+C to quit -> SIGINT?
 docker stop -> SIGTERM
 docker kill -> S??


- just want SIGNALS handling and child processes handling.

- ``init`` 
init run an init process (PID 1) inside the container that forwards signals and reaps processes. Set this option to true to enable this feature for the service.



 ---

 ## References
 
 1. How to gracefully stop FastAPI app: https://github.com/tiangolo/fastapi/issues/2928
 2. Choosing an init process for multi-process containers: https://ahmet.im/blog/minimal-init-process-for-containers/
 3. How To Use Signal Driven Programming In Applications: https://medium.com/fintechexplained/advanced-python-how-to-use-signal-driven-programming-in-applications-84fcb722a369
 4. signal — Set handlers for asynchronous events: https://docs.python.org/3/library/signal.html (see https://pythonhosted.org/blinker/)
 5. Understanding Docker Container Exit Codes: https://betterprogramming.pub/understanding-docker-container-exit-codes-5ee79a1d58f6
 6. 