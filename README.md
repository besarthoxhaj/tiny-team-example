## Tiny Team


```sh
$ apt install -y python3.8-venv
$ python3.8 -m venv env
$ source env/bin/activate
$ pip install fastapi
$ pip install "uvicorn[standard]"
$ pip install redis
$ pip install psycopg2-binary
$ pip install confluent-kafka
# once done installing, save the packages
# in a "requirements.txt" file
$ pip freeze > requirements.txt
# next time they can be installed directly
$ pip install -r requirements.txt
```


```sh
$ uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
$ curl -X POST "http://localhost:7777/item" -H "Content-Type: application/json" -d '"Hello, Redis!"'
# {"status": "success"}
$ curl "http://localhost:7777"
# {"status": "Hello, Redis!"}
```


## Install and Run

Make sure to install Docker before installing Docker Compose. Follow
the instructions at https://docs.docker.com/engine/install/ubuntu/ then
come back and continue below.


```sh
$ curl -SL https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
$ curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
$ tilt up --host 0.0.0.0 --port 10350
# or use normal docker compose
$ docker-compose up -d
```

## Services


```sh
$ open http://[HOST_IP_ADDRESS]:8002 # RedisInsight
$ open http://[HOST_IP_ADDRESS]:9080 # Kafka Dashboard
```

## Workbench

Visual Studio Code has a Jupyter extension which allows you to write
code directly on a python file and by adding `#%%` transform it in
an interactive cell. Try it out :)

It is recommended to install Miniconda in order to manage the different
environments and packages. Below the installation instructions.

```sh
$ wget -P ~/ https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
$ chmod +x ~/Miniconda3-latest-Linux-x86_64.sh
$ ~/Miniconda3-latest-Linux-x86_64.sh -b
$ export PATH=~/miniconda3/bin:$PATH
$ conda init
# IMPORTANT: close and start a new session
$ conda config --set auto_activate_base false
```

Then you will have access to a conda enviorment. Try few commands
to make sure everything works as expected

```sh
$ conda env list
$ conda create --name tiny python=3.8 -y
$ conda activate tiny
$ conda install -y pytorch torchvision torchaudio cpuonly -c pytorch
```

## Scripts

```sh
$ ./scripts/setup_exporter.sh
$ source env/bin/activate
$ python scripts/create_pg_schema.py
```


## Dashboards

Prometheus and Grafana are the two main tools used for
real-time analytics and monitoring. Read more:

- https://prometheus.io/
- https://grafana.com/docs/
- https://grafana.com/docs/grafana/latest/administration/provisioning/#dashboards
