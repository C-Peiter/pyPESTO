import pytest
from pypesto.modelselection.row2problem import *
from pypesto.petab import PetabImporter
import petab
import pandas as pd
import csv

YAML_FILENAME_COLUMN = "SBML"
MODEL_NAME_COLUMN = "modelId"

@pytest.fixture
def modelselection_file_example():
    return "doc/example/model_selection/modelSelectionSpecification_example_" \
           "modelSelection.tsv"


@pytest.fixture
def yaml_file_example():
    return "doc/example/model_selection/example_modelSelection.yaml"


@pytest.mark.xfail  # example does not seem to compile properly yet
def test_row2problem_yaml_string(yaml_file_example):
    petab_problem = petab.Problem.from_yaml(yaml_file_example)

    importer = PetabImporter(petab_problem)
    obj = importer.create_objective()
    pypesto_problem = importer.create_problem(obj)

    row = pd.Series()
    assert row2problem(row, yaml_file_example) == pypesto_problem


@pytest.mark.xfail  # example does not seem to compile properly yet
def test_row2problem_setting_pars(yaml_file_example,
                                  modelselection_file_example):
    with open(modelselection_file_example, newline='') as file:
        for row in csv.DictReader(file, delimiter='\t'):
            for key, value in row.items():
                if key == MODEL_NAME_COLUMN or key == YAML_FILENAME_COLUMN:
                    continue
                else:
                    row[key] = float(value)

            returned_problem = row2problem(dict(row), yaml_file_example)

            for key in [YAML_FILENAME_COLUMN, MODEL_NAME_COLUMN]:
                row.pop(key)
            x_names = list(row.keys())

            x_free_indices = [list(row).index(key) for key, value in row.items() if np.isnan(value)]
            x_fixed_indices = [list(row).index(key) for key, value in row.items() if not np.isnan(value)]
            x_fixed_vals = [value for key, value in row.items() if not np.isnan(value)]

            assert (returned_problem.x_names == x_names and returned_problem.x_free_indices == x_free_indices
                    and returned_problem.x_fixed_indices == x_fixed_indices and returned_problem.x_fixed_vals == x_fixed_vals)