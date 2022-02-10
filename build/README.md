# Avo Assure CI

Azure Pipelines is configured on many pre-defined variables.
Changing these during triggering build will yeild desired package.

## Variables

## Library Variables

| Variables | Description | Expected Value | Current Value |
|-----------|-------------|----------------|---------------|
| MAJOR_VERSION | ICE major release version (**x**.y.z) | Integer | 3 |
| MINOR_VERSION | ICE minor release version (x.**y**.z) | Integer | 5 |
| BUILD_PYC | The files that should be built as pyc instead of pyd. | <file_path1>;<file_path2>;<file_path3>;... (Rel. to plugins folder) | AWS/android_operations_keywords.py;AWS/android_spinner_keywords.py;AWS/custom_aws.py;AWS/generic_operations.py;AWS/testmobile_constants.py |
| BUILD_IGNORE | The files that should be left as py file itself. | <file_path1>;<file_path2>;<file_path3>;... (Rel. to plugins folder) | Core/\_\_main\_\_.py |


## Runtime Variables

| Variables | Description | Expected Value | Default Value |
|-----------|-------------|----------------|---------------|
| PROD_BUILD | Build & version generated is to be RC or prod ready | Boolean | false |
| LOG_VERSION | Push current ICE builld version in WebServer-ICE manifest or not | Boolean | true |
| DELTA_FILES | Should package be complete (baseline) or just changed files as compared to last release | Boolean | true |


## SOFTWARES NEEDED
* `WinBuild 32/64`
* `7z`
* `Python`
* `Pip Package - Cython`
