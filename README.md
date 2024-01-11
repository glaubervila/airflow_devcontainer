# airflow_devcontainer


https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

```bash
gh repo clone glaubervila/airflow_devcontainer
```

```bash
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

```bash
docker compose up airflow-init
```

```bash
docker compose up
```

