 # Control Core

<p align="center">
 <img src="img/overview.min.png" width=300 class="center"/>
</p>

---

 ## Use case: *control* loop with two nodes
 
 Created two interacting nodes (I renamed them "*control*" and "*PM*")

<p align="center">
<img src="img/schematic.min.png" width=100 />
</p>


### draft 1
 They each do a silly computation:

 1. *control* increments the output of *PM* (``y``) by one and this result (``x``) is the input to *PM* 
 2. *PM* increments its input (``x``) by ``0.5`` and this result is the input to *control*.
 3. To keep it from being an infinite loop, they both terminate when ``x>10``, and reset their values back to ``0`` (so I can rerun the notebook easily).

When I first start one node, it is just stuck at ``0``, but when I start the other node, they progress such that ``x`` is always one larger than ``y``

<p align="center">
<img src="img/osparc.min.png" width=300 />
</p>

### draft 2

- As draft 1 but one dedicated time heartbeat + array of weights for optimization for inputs/outputs
  - controller: (MPC algorithm using cvxopt) 
    - input #1: simtime, ym (heart rate, pressure)
    - input #2 configuration matrices
    - output #1: simtime, u (stimulations to heart) 
  - PM (simplified cardiac model) 
    - input #1: simtime, u 
    - input #2: configuration matrices
    - output #1: simtime, ym (for next heartbeat, ie time advances)
    <p align="center">
    <img src="img/osparc-cl.min.png" width=400 />
    </p>
### draft 3

- Untested idea:  Sleeping with standard I/O in Jupyter Lab?


### Interfaces to container

<p align="center">
<img src="img/container-interface.min.png" width=400>
</p>
