
from benchmark_runner.main.environment_variables import *
from benchmark_runner.common.logger.logger_time_stamp import logger_time_stamp, logger
from benchmark_runner.benchmark_operator.benchmark_operator_workloads import BenchmarkOperatorWorkloads
from benchmark_runner.main.environment_variables import environment_variables

# logger
log_level = os.environ.get('log_level', 'INFO').upper()
logger.setLevel(level=log_level)

# venv
# python -m venv venv
# . venv/bin/activate


@logger_time_stamp
def main():
    """
    The main
    """
    environment_variables_dict = environment_variables.environment_variables_dict
    workload = environment_variables_dict.get('workload', '')
    # workload name validation
    if workload not in environment_variables.workloads_list:
        logger.info(f'Enter valid workload name {environment_variables.workloads_list}')
        raise Exception(f'Not valid workload name: {workload} \n, choose one from the list: {environment_variables.workloads_list}')

    es_host = environment_variables_dict.get('elasticsearch', '')
    es_port = environment_variables_dict.get('elasticsearch_port', '')
    kubeadmin_password = environment_variables_dict.get('kubeadmin_password', '')
    benchmark_operator_workload = BenchmarkOperatorWorkloads(kubeadmin_password=kubeadmin_password, es_host=es_host, es_port=es_port)
    # benchmark-operator node selector
    if environment_variables_dict.get('pin_node_benchmark_operator'):
        benchmark_operator_workload.update_node_selector(runner_path=environment_variables_dict.get('runner_path', ''),
                                                         yaml_path='benchmark-operator/config/manager/manager.yaml',
                                                         pin_node='pin_node_benchmark_operator')
    benchmark_operator_workload.run_workload(workload=workload)


main()

