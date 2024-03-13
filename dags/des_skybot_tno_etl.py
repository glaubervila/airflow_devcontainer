import sys
sys.path.append("/opt/airflow")
from airflow.models import DAG
from airflow.decorators import dag, task
# from airflow.operators.python import PythonOperator
from pprint import pprint
import pendulum
import logging
import requests
from urllib.parse import urljoin
from pathlib import Path
import json
import time
import pandas as pd
# from operators.skybot_operator import SkybotOperator

base_path = Path("/opt/airflow/data/skybot")
database_path = Path("/opt/airflow/data/skybot/database")

# Radius usado na query do skybot com tamanho suficiente para a exposição do des.
# Cone search radius in Degres
radius = 1.2
# Date Correction for DECam
date_correction = 1.05
# Observer Code for Cerro Tololo-DECam
observer_location = "w84"
# Filter to retrieve only objects with a position error lesser than the given value
position_error = 0


@dag(
    schedule=None,
    start_date=pendulum.datetime(2024, 3, 1, tz="UTC"),
    catchup=False,
)
def des_skybot_tno_etl():
    """DES x Skybot ETL for Solar System Portal"""
   
    # Prepare 
    # ------------------------------------------------
    @task()
    def prepare(**kwargs) -> list:
        """Criar pastas
        Verificar se os arquivos estao disponiveis.
        Ler os arquivos/Converter
        """
        # Create Job path
        job_path = base_path.joinpath(f"{{ ds_nodash }}")
        job_path.mkdir(parents=True, exist_ok=True)

        # https://pythonspeed.com/articles/pandas-read-csv-fast/
        # https://saturncloud.io/blog/how-to-efficiently-read-large-csv-files-in-python-pandas/#:~:text=Use%20Chunking,into%20memory%20at%20a%20time.
        exposures_csv = database_path.joinpath("exposures.csv")
        # exposures_pq = database_path.joinpath("exposures.parquet")
        df = pd.read_csv(exposures_csv, nrows=2, delimiter='|', usecols=["id", "date_obs", "radeg", "decdeg", "exptime"])
               
        # TODO: Aplicar correção na date_obs
        df["date_with_correction"] =  df['date_obs']

        exposures = df.to_dict(orient='records')

        logging.info(f"Exposures: {len(exposures)}")
        logging.debug(list(exposures))

        return list(exposures)


    # skybot = SkybotOperator(
    #         task_id="skybot_cone_search",
    #         exposure_id="{{ ti.xcom_pull(task_ids='prepare', key='id') }}",
    #         date="{{ ti.xcom_pull(task_ids='prepare', key='date_with_correction') }}",
    #         ra=0, 
    #         dec=0,
    #         radius=radius,
    #         observer_location=observer_location,
    #         position_error=position_error,
    #         output_path = Path(f"data/skybot/1/cone_search_outputs"))

    # Extract (Sequencial 1 exposure por vez)
    # ------------------------------------------------
    @task()
    def extract(exposure: dict) -> int:
        """Para cada exposure:
          agrupar os ccds. 
          fazer a consulta no Skybot
          gerar arquivo com o retor no skybot.
        
        """
        # logging.info(exposure)
        # to = SkybotOperator(
        #     exposure_id=exposure['id'],
        #     date=exposure['date_with_correction'],
        #     ra=exposure['radeg'], 
        #     dec=exposure['decdeg'],
        #     radius=radius,
        #     observer_location=observer_location,
        #     position_error=position_error,
        #     output_path = Path(f"data/skybot/{{ ds_nodash }}/cone_search_outputs"))
        return exposure['id']

    # Transform
    # ------------------------------------------------
    @task()
    def transform(id: int) -> int:
        logging.info(f"Teste ID: {id}")
        return id

    # Load
    # ------------------------------------------------
    @task()
    def load(ids: list) -> None:
        logging.info(f"Load Task!")
        logging.info(f"Count IDS: {len(ids)}")


    # Clean
    # ------------------------------------------------
    @task()
    def clean() -> None:
        logging.info(f"Clean Taks!")

    
    # Pipeline
    # ------------------------------------------------
    # exposures = prepare()
    # https://github.com/apache/airflow/discussions/30785
    # ids = extract.expand(exposure=prepare()) 
    # new_ids = transform.expand(id=ids)
    # load(new_ids) >> clean()
       




    # TEST WITH CUSTON OPERATOR
    # https://docs.astronomer.io/learn/airflow-importing-custom-hooks-operators
    exposures = prepare() 
    # ids = extract.expand(exposure=prepare()) 


    # df = pd.read_parquet(paths["exposures_file"], engine="fastparquet")
    # df = pd.read_parquet(paths["exposures_file"])
    # print(df.head())

    # extract(paths) >> transform() >> load() >> clean()

des_skybot_tno_etl()