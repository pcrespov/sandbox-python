

### /containers/

- create(docker-compose) -> 202
  - POST /containers
  - docker-compose config -f {}; docker-compose up -f {} --no-start
- list
  - GET  /containers
- read(id)
  - GET  /containers/{id}
- ~~update~~
- ~~delete~~
- up
  - POST  /containers:up
  - means (pull) create + start containers
- down
  - POST  /containers:down
  - means stop + remove containers



### /containers/logs
- list
  - GET /containers/logs
  - means docker-compose logs

### /containers/{id}/logs
- read
  - GET /containers/{id}/logs
  - means docker-compose logs {id}

###  /compose/{}/docker/[...]
    Reverse proxy to docker engine API





https://docs.docker.com/engine/api/v1.30/



### POST /containers/{id}/docker API engine -> docker engine docker API



https://app.swaggerhub.com/apis/deviantony/Portainer/2.0.1#/settings/get_settings_public

Execute Docker requests
Portainer DO NOT expose specific endpoints to manage your Docker resources (create a container, remove a volume, etc...).

Instead, it acts as a reverse-proxy to the Docker HTTP API. This means that you can execute Docker requests via the Portainer HTTP API.

To do so, you can use the /endpoints/{id}/docker




-----

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