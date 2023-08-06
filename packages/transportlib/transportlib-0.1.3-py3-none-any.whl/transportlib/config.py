import importlib
import logging
from pathlib import Path
import yaml


def read_config(path_to_config_file):
    with open(path_to_config_file, 'r') as file:
        tasks = yaml.load(file, Loader=yaml.FullLoader)

    return tasks


def get_task_by_name(
        tasks,
        target_name,
):
    task = None
    for candidate_task in tasks:
        candidate_name = candidate_task.get('name')

        if target_name == candidate_name:
            task = candidate_task

    if task is None:
        task = {}

    return task


def execute_config_task(task):
    output_folder = Path('output')
    output_folder.mkdir(exist_ok=True, parents=True)

    csv_file_name = task.get('csv_file_name', '')
    csv_file_path = output_folder.joinpath(f'{csv_file_name}.csv')

    # Get Source Transport
    path_to_source_transport_module = task.get('source_transport', {}).get('path_to_module', '')
    source_transport_name = task.get('source_transport', {}).get('transport_name', '')
    source_transport_kwargs = task.get('source_transport', {}).get('kwargs', {})

    source_transport_kwargs.update({'csv_file_path': csv_file_path})

    source_transport_module = importlib.import_module(path_to_source_transport_module)
    source_transport = getattr(source_transport_module, source_transport_name)

    # Get Destination Transport
    path_to_destination_transport_module = task.get('destination_transport', {}).get('path_to_module', '')
    destination_transport_name = task.get('destination_transport', {}).get('transport_name', '')
    destination_transport_kwargs = task.get('destination_transport', {}).get('kwargs', {})
    destination_transport_kwargs.update({'csv_file_path': csv_file_path})

    destination_transport_module = importlib.import_module(path_to_destination_transport_module)
    destination_transport = getattr(destination_transport_module, destination_transport_name)

    if source_transport is None:
        raise ValueError('No Source Transport is specified!!!')

    if destination_transport is None:
        raise ValueError('No Destination Transport is specified!!!')


    # Run Source
    source_transport(**source_transport_kwargs).run()
    destination_transport(**destination_transport_kwargs).run()

