# Dynamic Sydecar API Rationale

The API essentialy evolves around some parts of the docker-compose CLI

```
 docker-compose --help
Define and run multi-container applications with Docker.

Usage:
  docker-compose [-f <arg>...] [options] [--] [COMMAND] [ARGS...]
  docker-compose -h|--help

Options:
  -f, --file FILE             Specify an alternate compose file
                              (default: docker-compose.yml)
  -p, --project-name NAME     Specify an alternate project name
                              (default: directory name)
  -c, --context NAME          Specify a context name
  --verbose                   Show more output
  --log-level LEVEL           Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  --no-ansi                   Do not print ANSI control characters
  -v, --version               Print version and exit
  -H, --host HOST             Daemon socket to connect to

  --tls                       Use TLS; implied by --tlsverify
  --tlscacert CA_PATH         Trust certs signed only by this CA
  --tlscert CLIENT_CERT_PATH  Path to TLS certificate file
  --tlskey TLS_KEY_PATH       Path to TLS key file
  --tlsverify                 Use TLS and verify the remote
  --skip-hostname-check       Don't check the daemon's hostname against the
                              name specified in the client certificate
  --project-directory PATH    Specify an alternate working directory
                              (default: the path of the Compose file)
  --compatibility             If set, Compose will attempt to convert keys
                              in v3 files to their non-Swarm equivalent (DEPRECATED)
  --env-file PATH             Specify an alternate environment file

Commands:
  build              Build or rebuild services
  config             Validate and view the Compose file
  create             Create services
  down               Stop and remove containers, networks, images, and volumes
  events             Receive real time events from containers
  exec               Execute a command in a running container
  help               Get help on a command
  images             List images
  kill               Kill containers
  logs               View output from containers
  pause              Pause services
  port               Print the public port for a port binding
  ps                 List containers
  pull               Pull service images
  push               Push service images
  restart            Restart services
  rm                 Remove stopped containers
  run                Run a one-off command
  scale              Set number of containers for a service
  start              Start services
  stop               Stop services
  top                Display the running processes
  unpause            Unpause services
  up                 Create and start containers
  version            Show version information and quit

```


So using our API Design Guidelines, we suggest a more [resource oriented design](https://cloud.google.com/apis/design/resources). For each collection or resource we start with [standard](https://cloud.google.com/apis/design/standard_methods) methods (i.e. CRUD) followed by [custom](https://cloud.google.com/apis/design/custom_methods) methods.


### /containers collection

- **C**reate(compose_file) -> 202
  - ``POST /containers``
  - docker-compose config -f {}; docker-compose up -f {} --no-start
- **R**ead(id)
  - get item
    - ``GET  /containers/{id}``
  - list iterms
    - ``GET  /containers``
- ~~**U**pdate~~
- ~~**D**elete~~
- up
  - ``POST  /containers:up``
  - means (pull) + create + start containers
- down
  - ``POST  /containers:down``
  - means stop + remove containers



### /containers/logs
- list
  - ``GET /containers/logs``
  - means ``docker-compose logs``

### /containers/{id}/logs 

- read
  - ``GET /containers/{id}/logs``
  - means ``docker-compose logs {id}``

    Reverse proxy to docker engine API

etc ...

### /docker/containers/{id}/*

- ``POST /containers/{id}/docker`` 
- Allows direct access to the [docker engine HTTP API](https://docs.docker.com/engine/api/v1.30/#tag/Container) on the sidecar host
- Special entrypoint useful to **develop prototypes** that can be later "frozen" in a separate entrypoint.
- This approach is found in portainer. It DOES NOT exposes specific endpoints to manage your Docker resources (create a container, remove a volume, etc...). Instead, it acts as a reverse-proxy to the [Docker HTTP API](https://docs.docker.com/engine/api/v1.30/). This means that you can execute Docker requests via the [Portainer HTTP API](https://app.swaggerhub.com/apis/deviantony/Portainer/2.0.1#/settings/get_settings_public)



SEE [docker engine HTTP API](https://docs.docker.com/engine/api/v1.30/#tag/Container)


# Running code

```cmd
python -m venv .venv; source venv/bin/activate
make install
make up
```

Open http://0.0.0.0:8000/  to see the swagger and look at the details of the specs (e.g. errors etc)