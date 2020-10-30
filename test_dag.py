from airflow.operators.bash_operator import BashOperator
from airflow.models import DAG
from datetime import datetime, timedelta
from pytz import timezone

dateformat = '%Y-%m-%d'
today = datetime.now(timezone('Asia/Seoul'))
yesterday = today - timedelta(1)

args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 10, 23),
    'retries': 1,
    'retry_delay': timedelta(minutes=120)
}


dag = DAG(
    dag_id='test_dag',
    catchup=False,
    default_args=args,
    schedule_interval="@once")

# Bash Operator
cmd1 = 'python /home/admin_jang/Airflow/get_price_airflow.py'
t1 = BashOperator(task_id='get_price',
                  bash_command=cmd1,
                  dag=dag)

cmd2 = 'python /home/admin_jang/Airflow/get_fs_airflow.py'
t2 = BashOperator(task_id='get_fs',
                  bash_command=cmd2,
                  dag=dag)

cmd3 = 'python /home/admin_jang/Airflow/get_bond_airflow.py'
t3 = BashOperator(task_id='get_bond',
                  bash_command=cmd3,
                  dag=dag)

# t1 >> t2
t2.set_upstream(t1)
