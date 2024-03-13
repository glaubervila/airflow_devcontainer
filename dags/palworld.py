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

log = logging.getLogger(__name__)


@dag(
    schedule=None,
    start_date=pendulum.datetime(2024, 2, 1, tz="UTC"),
    catchup=False,
)
def palworld_data_mining():
    """Palworld Data Mining"""

    def get_json_data(url):
        # log.info("Passou aqui")
        # pprint(kwargs)
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            raise Exception(r.status_code)
        return r.json()
    
    def download_json_data(url, filepath): 
        data = get_json_data(url)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f)

    @task()
    def get_main_urls(df=None, **kwargs) -> dict:
        index_url = 'https://palworldtrainer.com/_nuxt/builds/meta/fd149cec-6187-4860-916d-389f5f3d12d2.json'
        index = get_json_data(index_url)
        urls = index['prerendered']
        
        base_url = 'https://palworldtrainer.com'
        dirs = ['/pal/', '/items/']
        result = {}
        for d in dirs:
            if d not in result:
                result[d] = []

            for url in urls:
                if url.startswith(d):
                    print(url)
                    json_url = urljoin(base_url, f"{url}/_payload.json")
                    result[d].append(json_url)


        return result

    @task()
    def get_pals_url(urls):
        for url in urls:
            # print(url)
            base_path = Path('/opt/airflow/data/pal')
            filepath = base_path.joinpath(url.split('/pal/')[1])
            # print(filepath)
            # download_json_data(url, filepath)

    @task()
    def get_items_url(urls):
        for url in urls:
            # print(url)
            base_path = Path('/opt/airflow/data/items')
            filepath = base_path.joinpath(url.split('/items/')[1])
            download_json_data(url, filepath)
            time.sleep(0.3)

    urls = get_main_urls()

    [get_pals_url(urls['/pal/']),  get_items_url(urls['/items/'])]

    # pprint(urls)


palworld_data_mining()