from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
import pendulum


default_args = {
    'owner': 'GTamara',
    'depends_on_past': False,
    'start_date': pendulum.datetime(2025,1,1,2,tz='Asia/Yekaterinburg')
}

SHORT_DESCRIPTION = 'Загрузка курса обмена валют'

LONG_DESCRIPTION = '''
Загрузка курса обмена валют.
'''

with DAG('daily_curs_load',
         default_args=default_args, 
         schedule='0 3 * * *', 
         catchup=True,
         max_active_runs=1, 
         max_active_tasks=1, 
         tags=['DE_projects']) as dag:

    start = EmptyOperator(
        task_id = 'start_task'
    )

    load_dict = BashOperator(
        task_id = 'ETL_curs_data',
        bash_command='/home/toma/DE_projects/afvenv/bin/python3 /home/toma/airflow/scripts/daily_curs_dag/task1.py --date {{ds}}',
    )

    end = EmptyOperator(
        task_id = 'end_task'
    )

start >> load_dict >> end