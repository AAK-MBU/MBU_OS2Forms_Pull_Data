"""This module contains the main process of the robot."""
import json

from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection

from mbu_dev_shared_components.os2forms import forms
from mbu_dev_shared_components.utils.db_stored_procedure_executor import execute_stored_procedure


def process(orchestrator_connection: OrchestratorConnection) -> None:
    """Do the primary process of the robot."""
    orchestrator_connection.log_trace("Running process.")
    orchestrator_connection.log_trace("TEST!!.")
    oc_args_json = json.loads(orchestrator_connection.process_arguments)
    orchestrator_connection.log_trace(oc_args_json)
    sql_conn_string = orchestrator_connection.get_constant('DbConnectionString').value
    orchestrator_connection.log_trace(sql_conn_string)
    api_key = orchestrator_connection.get_credential("os2_api").password

    response = forms.get_list_of_active_forms(oc_args_json['OS2FormsEndpoint'], oc_args_json['DataWebformId'], api_key)
    orchestrator_connection.log_trace(response)
    forms_dict = response.json()['submissions']
    for key in forms_dict:
        orchestrator_connection.log_trace("FOR EACH")
        form_url = forms_dict[key]

        forms_response = forms.get_form(form_url, api_key)

        reference = forms_response.json()['entity']['uuid'][0]['value']
        completed = forms_response.json()['entity']['completed'][0]['value']
        data = json.dumps(forms_response.json(), ensure_ascii=False)

        sql_params = {
            "tableName": ("str", f'{oc_args_json["TableName"]}'),
            "reference": ("str", f'{reference}'),
            "creation_time": ("datetime", f'{completed}'),
            "data": ("str", f'{data}')
        }

        execute_stored_procedure(sql_conn_string, oc_args_json['SPName'], sql_params)


if __name__ == "__main__":
    oc = OrchestratorConnection.create_connection_from_args()
    process(oc)
