# energy_barrier_problem
DNA energy barrier problem solver and sample generator using Google OR-Tools

## Environment values
#### NUMBER_OF_THREADS
    number of threads to use for the solver
#### NUMBER_OF_VERTICES
    number of vertices in the sample graph
#### NUMBER_OF_SAMPLES
    number of output samples to generate
#### MIN_NUMBER_OF_EDGES
    minimum number of edges in the graph during generation phase
#### MAX_NUMBER_OF_EDGES
    maximum number of edges in the graph  during generation phase
#### DB_NAME
    name of the database


## Build the project
```shell
docker compose build
```
## Run the project
```shell
docker compose up [-d]
```
