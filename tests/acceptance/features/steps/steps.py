import os
import yaml
import json
import glob
import shutil
from pathlib import Path
from behave import given, when, then

from sdg import SDG
from tests.acceptance.features.environment import DEFAULTS


@given('the metadata file exists locally with columns')
def step_imp(context):
    """
    Creates the metadata from the context table and saves it with the format of YAML and JSON
    """
    columns = []
    for row in context.table:
        columns.append({
            "name": row[0],
            "type": row[1],
            "args": eval(row[2]) if row[2] else None,
            "seed": int(row[3]),
            "null_probability": float(row[4]),
            "unique": eval(row[5])
        })

    metadata = {
        "columns": columns,
        "file_name": "test-file-1",
        "format": "csv"
    }

    if not os.path.exists(DEFAULTS.data_file):
        Path(DEFAULTS.data_file).mkdir(parents=True, exist_ok=True)

    # Write the files as yaml, yml and json
    with open(f"{DEFAULTS.json_metadata_path}", 'w+') as f:
        f.write(json.dumps(metadata))

    with open(f"{DEFAULTS.yml_metadata_path}", 'w+') as f:
        f.write(yaml.dump(metadata))

    with open(f"{DEFAULTS.yaml_metadata_path}", 'w+') as f:
        f.write(yaml.dump(metadata))


@given('the {metadata_file_type} metadata exists as a local file')
def step_imp(context, metadata_file_type: str):
    if metadata_file_type == 'JSON':
        assert os.path.exists(DEFAULTS.json_metadata_path)
    if metadata_file_type == 'YAML':
        assert os.path.exists(DEFAULTS.yaml_metadata_path)
    if metadata_file_type == 'YML':
        assert os.path.exists(DEFAULTS.yml_metadata_path)


@when('the user creates one local CSV sample file of 5 rows from {metadata_file_type} metadata')
def step_imp(context, metadata_file_type):

    if metadata_file_type == 'JSON':
        metadata_path = DEFAULTS.json_metadata_path
    elif metadata_file_type == 'YAML':
        metadata_path = DEFAULTS.yaml_metadata_path
    elif metadata_file_type == 'YML':
        metadata_path = DEFAULTS.yml_metadata_path
    else:
        raise ValueError(f"Metadata file type {metadata_file_type} not implemented")

    sdg = SDG(
        metadata=metadata_path
    )
    sdg.write(
        path=DEFAULTS.data_file,
        rows=5
    )


@then('one csv file is created')
def step_imp(context):
    files = glob.glob(f'{DEFAULTS.data_file}/test-file-1.csv')
    assert len(files) == 1


@then('the content of the csv file is')
def step_imp(context):

    csv_data = []
    with open(f'{DEFAULTS.data_file}/test-file-1.csv', 'r') as f:
        for line in f.readlines():
            csv_data.append(line.replace('\n', '').split(','))

    behave_data = [context.table.headings]
    for row in context.table:
        behave_data.append(list(row))

    # Uncomment for debug
    # print('CSV DATA ======')
    # print(csv_data)
    #
    # print('BEHAVE DATA ======')
    # print(behave_data)

    assert csv_data == behave_data
