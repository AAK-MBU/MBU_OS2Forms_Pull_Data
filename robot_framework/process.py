"""This module contains the main process of the robot."""
from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection


def process(orchestrator_connection: OrchestratorConnection) -> None:
    """Do the primary process of the robot."""
    orchestrator_connection.log_trace("Running process.")
    orchestrator_connection.log_trace("TEST!!.")
    #  oc_args_json = json.loads(fr'{orchestrator_connection.process_arguments}')
    sql_conn_string = orchestrator_connection.get_constant('DbConnectionString').value
    orchestrator_connection.log_trace(sql_conn_string)
    api_key = orchestrator_connection.get_credential("os2_api").password
    orchestrator_connection.log_trace(len(api_key))


if __name__ == "__main__":
    oc = OrchestratorConnection.create_connection_from_args()
    process(oc)
