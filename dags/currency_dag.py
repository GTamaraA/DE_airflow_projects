from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
import pendulum


default_args = {
    'owner': 'GTamara',
    'depends_on_past': False,
    'start_date': pendulum.datetime(2026,4,28,3,tz='Asia/Yekaterinburg')
}

SHORT_DESCRIPTION = 'Загрузка справочника валют'

LONG_DESCRIPTION = '''
Загрузка справочника валют.
'''

with DAG('get_currency',
         default_args=default_args, 
         schedule='0 1 2 * *', 
         catchup=False,
         max_active_runs=1, 
         max_active_tasks=1, 
         tags=['DE_projects']) as dag:

    start = EmptyOperator(
        task_id = 'start_task'
    )

    load_dict = BashOperator(
        task_id = 'get_dict',
        bash_command='/home/toma/DE_projects/afvenv/bin/python3 /home/toma/airflow/scripts/currency_dag/task1.py',
    )

    end = EmptyOperator(
        task_id = 'end_task'
    )
