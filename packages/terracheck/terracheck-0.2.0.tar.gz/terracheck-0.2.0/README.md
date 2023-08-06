# Terracheck

A Python library to check Terraform style and structure good practices defined in 
[Google Coud Terraform sytel and practices documentation](https://cloud.google.com/docs/terraform/best-practices-for-terraform#general-style).

The code is Python 3. Compatibility with Python 2 has not been tested.

## Installation

Fast install:

```sh
pip install terracheck

```

Install the package:

```sh
python setup.py install

```

## Example

### StyleChecker

```python

    from terracheck.io.HclCheckerReader import HclCheckerReader
    from terracheck.checker.StyleChecker import StyleChecker

    # Read files in a HCL folder
    hcl_checker_reader = HclCheckerReader()
    hcl_checker_reader.read("/hcl/folder/path")

    # Check style good practices
    style_checker = StyleChecker()
    style_checker.check(hcl_checker_reader.extract)
    
    style_report = style_checker.report

    style_metadata = style_checker.metadata
 ```

An output example :

```sh
    [DASH_IN_NAME]: Name of variable named 'gcp-folder_parent_id' contains dash ('-'). Shoud be underscores ('_').
    [DASH_IN_NAME]: Name of data 'google_storage_bucket' 'google-storage_bucket' contains dash ('-'). Shoud be underscores ('_').
    [DASH_IN_NAME]: Name of resource 'google_storage_bucket' 'google-storage_bucket' contains dash ('-'). Shoud be underscores ('_').
    [DASH_IN_NAME]: Name of output named 'my-output' contains dash ('-'). Shoud be underscores ('_').
    [NAME_IS_RESOURCE]: Resource 'google_storage_bucket' is named 'google_storage_bucket'. Chose a name different than the resource name.
    [FILE_PURPOSE]: Required_providers 'google' should be declared in file versions.tf not in version.tf.
    [FILE_PURPOSE]: Variable 'gcp-folder_parent_id' should be declared in file variables.tf not in hcl_2.tf.
    [FILE_PURPOSE]: Output 'my-output' should be declared in file outputs.tf not in hcl_1.tf.
    [FILE_PURPOSE]: Required_providers 'google-beta' should be declared in file versions.tf not in variables.tf.
    [FILE_PURPOSE]: Required_providers 'gitlab' should be declared in file versions.tf not in variables.tf.
    [FILE_PURPOSE]: Provider 'gitlab' should be declared in file versions.tf not in variables.tf.
    [OUTPUT_EXPOSURE]: Output 'cycling_output' references a variable as value. It should not.
    [NAME_UNIQUENESS]: Resource 'google_bigquery_dataset' is unique, and thus should be named 'main', not 'dataset'.
    [NAME_UNIQUENESS]: Resource 'google_service_account' is unique, and thus should be named 'main', not 'bqowner'.
```

### StructureChecker

```python

    from terracheck.checker.StructureChecker import StructureChecker
    
    structure_checker = StructureChecker("/checker/config/path")

    structure_checker.check("/hcl/folder/path")

    structure_report = structure_checker.report

    structure_metadata = structure_checker.metadata
```

With respect to the following hcl folder structure:

```sh
demo_hcl_folder
   | google-hcl_1.tf
   | hcl_2-org.tf
   | outputs.tf
   | variables.tf
   | version.tf
```

and the following ```StructureChecker``` config:

```yaml
mandatory_files:
  version:
    - "versions.tf"
  readme:
    - "README.MD"
    - "README.md"

filenames_nomenclature:
  startswith: "google"
  endswith: "org"
  contains: "-"
```

the output is :

```sh
    [MISSING_FILE]: File 'version' is missing in your terraform folder. Available denominations : ['versions.tf'].
    [MISSING_FILE]: File 'readme' is missing in your terraform folder. Available denominations : ['README.MD', 'README.md'].
    [FILENAME_CONSTRAINT]: File 'google-hcl_1.tf' does not respect constraint 'endswith org'.
    [FILENAME_CONSTRAINT]: File 'version.tf' does not respect constraint 'startswith google'.
    [FILENAME_CONSTRAINT]: File 'version.tf' does not respect constraint 'endswith org'.
    [FILENAME_CONSTRAINT]: File 'version.tf' does not respect constraint 'contains -'.
    [FILENAME_CONSTRAINT]: File 'hcl_2-org.tf' does not respect constraint 'startswith google'.
    [FILENAME_CONSTRAINT]: File 'hcl_2-org.tf' does not respect constraint 'endswith org'.
```

### HCL Reader

As in examples bellow, HclCheckerReader reads from a folder path. But the content to check can 
also be extended from string HCL content :

````python

    import json
    from terracheck.io.HclCheckerReader import HclCheckerReader
    
    hcl_checker_reader = HclCheckerReader()
    
    file_path_1 = "/file/path/1"
    file_path_2 = "/file/path/2"
    
    with open(file_path_1, "r") as f:
        hcl_checker_reader.extend(f.read(), file_path_1)
    
    with open(file_path_2, "r") as f:
        hcl_checker_reader.extend(f.read(), file_path_2)
    
    for element_type, checker_element in hcl_checker_reader.extract.items():
        print(json.dumps(checker_element.to_dict(), indent=4))
````