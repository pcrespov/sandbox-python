#
# https://airflow.apache.org/docs/stable/tutorial.html#
#
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

# These are operator's defaults
# https://airflow.apache.org/docs/stable/_api/airflow/models/index.html#airflow.models.BaseOperator
#
#
default_args = {
    "owner": "airflow",
    "depends_on_past": False, #  individual task instances will depend on the success of their previous task instance 
    "start_date": days_ago(2),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}


dag = DAG("tutorial1", default_args=default_args)

t1 = BashOperator(task_id="date-printer", bash_command="date", dag=dag)
t2 = BashOperator(task_id="sleeper", bash_command="sleep 5", dag=dag)

templated_cmd = """
{% for i in range(5) %}
    echo "{{ ds }}"
    echo "{{ macros.ds_add(ds, 7)}}"
    echo "{{ params.my_param }}"
{% endfor %}
"""
t3 = BashOperator(
    task_id="templated", bash_command=templated_cmd, params={"x": 333}, dag=dag
)

t1 >> [t2, t3]
