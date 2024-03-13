# Airflow Devcontainer


https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html


Based on these articles

https://medium.com/@paulmartins/debugging-airflow-with-vscode-21dbd41d4de6

https://levelup.gitconnected.com/debugging-airflow-dags-in-containers-with-vs-code-e31c0e899c7e

https://davidgriffiths-data.medium.com/debugging-airflow-in-a-container-with-vs-code-7cc26734444


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

