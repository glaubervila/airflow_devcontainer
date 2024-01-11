from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
import pendulum

with DAG(
    'meu_primeiro_dag',
    start_date = pendulum.today('UTC').add(days=-1),
    schedule_interval='@daily'
) as dag:
    
    tarefa_1 = EmptyOperator(task_id='tarefa_1')
    tarefa_2 = EmptyOperator(task_id="tarefa_2")
    tarefa_3 = EmptyOperator(task_id="tarefa_3")
    tarefa_4 = EmptyOperator(task_id="tarefa_4")

    tarefa_1 >> [tarefa_2, tarefa_3]
    tarefa_3 >> tarefa_4