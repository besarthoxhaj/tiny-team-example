docker_compose([
  "./docker-compose-app.yml",
  "./docker-compose-monitor.yml",
  "./docker-compose-data.yml",
  "./docker-compose-kafka.yml",
], env_file=".env", project_name="tiny-team")

dc_resource("app",        labels=["app"])
dc_resource("worker",     labels=["app"])

dc_resource("kafka",      labels=["kafka"])
dc_resource("kafka-ui",   labels=["kafka"])

dc_resource("redis",      labels=["data"])
dc_resource("postgres",   labels=["data"])
dc_resource("pgadmin",    labels=["data"])

dc_resource("prometheus", labels=["monitor"])
dc_resource("exporter",   labels=["monitor"])
dc_resource("promlens",   labels=["monitor"])
dc_resource("grafana",    labels=["monitor"])
