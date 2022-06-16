

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
 3. 