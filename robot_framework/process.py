"""This module contains the main process of the robot."""
import json

from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection

from mbu_dev_shared_components.os2forms import forms
from mbu_dev_shared_components.utils.db_stored_procedure_executor import execute_stored_procedure


def process(orchestrator_connection: OrchestratorConnection) -> None:
    """Do the primary process of the robot."""
    orchestrator_connection.log_trace("Running process.")
    oc_args_json = json.loads(orchestrator_connection.process_arguments)
    sql_conn_string = orchestrator_connection.get_constant('DbConnectionString').value
    api_key = orchestrator_connection.get_credential("os2_api").password
    form_source = oc_args_json['form_source']
    destination_system = oc_args_json['destination_system']

    response = forms.get_list_of_active_forms(oc_args_json['os2_forms_endpoint'], oc_args_json['data_webform_id'], api_key)
    forms_dict = response.json()['submissions']
    for key in forms_dict:
        form_url = forms_dict[key]
        forms_response = forms.get_form(form_url, api_key)
        form_sid = forms_response.json()['entity']['sid'][0]['value']
        form_id = forms_response.json()['entity']['uuid'][0]['value']
        form_type = forms_response.json()['entity']['webform_id'][0]['target_id']
        form_submitted_date = forms_response.json()['entity']['completed'][0]['value']
        form_data = json.dumps(forms_response.json(), ensure_ascii=False)
        sql_params = {
            "form_sid": ("str", f'{form_sid}'),
            "form_id": ("str", f'{form_id}'),
            "form_type": ("str", f'{form_type}'),
            "form_source": ("str", f'{form_source}'),
            "form_data": ("str", f'{form_data}'),
            "form_submitted_date": ("str", f'{form_submitted_date}'),
            "destination_system": ("str", f'{destination_system}'),
        }
        execute_stored_procedure(sql_conn_string, oc_args_json['sp_name'], sql_params)
