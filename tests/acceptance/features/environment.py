import os
import yaml
import json
import glob
import shutil
from pathlib import Path
from dataclasses import dataclass
from behave import given, when, then
from behave import fixture


@dataclass
class DEFAULTS:
    data_file = 'acceptance_test_files'
    yaml_metadata_path = 'acceptance_test_files/metadata.yaml'
    yml_metadata_path = 'acceptance_test_files/metadata.yml'
    json_metadata_path = 'acceptance_test_files/metadata.json'


def after_scenario(context, scenario):
    print('Test complete. Removed all temporary files created within the test')
    shutil.rmtree(DEFAULTS.data_file)
