# Created by gabriel at 30/01/2023
Feature: Create CSV dataset

  Background:
    Given the metadata file exists locally with columns
      | column_name | column_type    | column_argument                                 | seed | null_prob | unique |
      | column-1    | random_element | {"elements": ["A", "B", "C"]}                   | 1    | 0         | False  |
      | column-2    | random_element | {"elements": ["A", "B", "C"]}                   | 1    | 0.3       | False  |
      | column-3    | numeric_id     | {"length": 8}                                   | 1    | 0         | False  |
      | column-4    | numeric_id     | {"length": 8}                                   | 1    | 0.3       | False  |
      | column-5    | numeric_id     | {"length": 8}                                   | 1    | 0         | True   |
      | column-6    | numeric_id     | {"length": 8}                                   | 1    | 0.3       | True   |
      | column-7    | string_id      | {"length": 8}                                   | 1    | 0         | False  |
      | column-8    | string_id      | {"length": 8}                                   | 1    | 0.3       | False  |
      | column-9    | string_id      | {"length": 8}                                   | 1    | 0         | True   |
      | column-10   | string_id      | {"length": 8}                                   | 1    | 0.3       | True   |
      | column-11   | string         | {"min_chars": 12, "max_chars": 24}              | 1    | 0         | False  |
      | column-12   | string         | {"min_chars": 12, "max_chars": 24}              | 1    | 0.3       | False  |
      | column-13   | string         | {"min_chars": 12, "max_chars": 24}              | 1    | 0         | True   |
      | column-14   | string         | {"min_chars": 12, "max_chars": 24}              | 1    | 0.3       | True   |
      | column-15   | integer        | {"min_value": -10000000, "max_value": 10000000} | 1    | 0         | False  |
      | column-16   | integer        | {"min_value": -10000000, "max_value": 10000000} | 1    | 0.3       | False  |
      | column-17   | integer        | {"min_value": -10000000, "max_value": 10000000} | 1    | 0         | True   |
      | column-18   | integer        | {"min_value": -10000000, "max_value": 10000000} | 1    | 0.3       | True   |
      | column-19   | boolean        |                                                 | 1    | 0         | False  |
      | column-20   | boolean        |                                                 | 1    | 0.3       | False  |
      | column-21   | date           | {"pattern": "%Y-%m-%d"}                         | 1    | 0         | False  |
      | column-22   | date           | {"pattern": "%Y-%m-%d"}                         | 1    | 0.3       | False  |
      | column-23   | date           | {"pattern": "%Y-%m-%d %H:%M:%S"}                | 1    | 0         | False  |
      | column-24   | date           | {"pattern": "%Y-%m-%d %H:%M:%S"}                | 1    | 0.3       | False  |

  Scenario Outline: User generates a CSV sample from a metadata file
    Given the <metadata_file_type> metadata exists as a local file
    When the user creates one local CSV sample file of 5 rows from <metadata_file_type> metadata
    Then one csv file is created
    And the content of the csv file is
      | column-1 | column-2 | column-3 | column-4 | column-5 | column-6 | column-7 | column-8 | column-9 | column-10 | column-11              | column-12                | column-13              | column-14                | column-15 | column-16 | column-17 | column-18 | column-19 | column-20 | column-21  | column-22  | column-23           | column-24           |
      | A        |          | 28034063 |          | 28034063 |          | gSNnzxHP |          | gSNnzxHP |           | DPdgNytkzUuFNK         |                          | DPdgNytkzUuFNK         |                          | -5491485  |           | -5491485  |           | True      |           | 1979-02-22 |            | 1979-02-22 15:23:38 |                     |
      | C        | A        | 86397250 | 18470054 | 86397250 | 18470054 | ebRwNaxL | SNnzxHPe | ebRwNaxL | SNnzxHPe  | LlXUbbCWtlvblwzm       | NnzxHPebRwNaxLlXUbbCWtlv | LlXUbbCWtlvblwzm       | NnzxHPebRwNaxLlXUbbCWtlv | 9099312   | -7882487  | 9099312   | -7882487  | False     | False     | 2008-09-25 | 2021-12-22 | 2008-09-25 15:20:05 | 2021-12-22 17:18:26 |
      | A        | A        | 18470054 | 25826780 | 18470054 | 25826780 | lXUbbCWt |          | lXUbbCWt |           | JNXWvVVfGLpMUYA        |                          | JNXWvVVfGLpMUYA        |                          | -7882487  | -6043305  | -7882487  | -6043305  | False     |           | 2021-12-22 |            | 2021-12-22 17:18:26 |                     |
      | B        | B        | 44234785 | 70329669 | 44234785 | 70329669 | lvblwzmm | wNaxLlXU | lvblwzmm | wNaxLlXU  | AVjoYzWuSyMvItTOMe     | NWCrJNXWvVVfGLp          | AVjoYzWuSyMvItTOMe     | NWCrJNXWvVVfGLp          | -1441304  | 5082417   | -1441304  | 5082417   | True      | True      | 1974-04-18 | 1978-01-09 | 1974-04-18 12:41:12 | 1978-01-09 21:14:44 |
      | A        | C        | 25826780 | 97455328 | 25826780 | 97455328 | lxpbRCHj |          | lxpbRCHj |           | AOBuzbcKZEuiAZOCSmAXEx | UYAYAVjoYzWuSyMvI        | AOBuzbcKZEuiAZOCSmAXEx | UYAYAVjoYzWuSyMvI        | -6043305  | 2737773   | -6043305  | 2737773   | True      | False     | 1987-05-11 | 2021-10-13 | 1987-05-11 18:36:14 | 2021-10-13 19:46:42 |
    Examples:
      | metadata_file_type |
      | JSON      |
      | YAML      |
      | YML       |
