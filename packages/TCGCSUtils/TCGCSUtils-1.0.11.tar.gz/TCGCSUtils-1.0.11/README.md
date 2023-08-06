<div id="logos">
    <p align="center">
        <img src="https://tc.com.br/wp-content/themes/tradersclub/img/tc-out.png" width="150" height="150">
    </p>
</div>   
<br>

<h1 align="center">TCGCSUtils</h1>
<h2 align="center">This lib was created to easily save and read files in GCS</h2>
<br>
<br>

<h1 align="left">Pip Install</h1>

```py
pip install TCGCSUtils
```

<br>

<h1 align="left">Authenticate</h1>

<h3>
 This lib has two ways to authenticate, you can use the Class parameters or use environment variables
</h3>

<h2>Class parameters</h2>

```py
from TCGCSUtils import GCSReader,GCSWriter

reader = GCSReader(
    gcp_project, # GCP Project
    service_account_info # Service account as json
)

writer = GCSWriter(
    gcp_project, # GCP Project
    service_account_info # Service account as json
)
```

<h2>Environment variables</h2>

```py
from TCGCSUtils import GCSReader,GCSWriter

reader = GCSReader()
writer = GCSWriter()
```

<h4>You don't need to pass the parameters through the function, but you need to make sure you environment has these variables:</h4>

```sh
GCP_PROJECT='PROJECT_ID'
GOOGLE_APPLICATION_CREDENTIALS='{YOUR_SERVICE_ACCOUNT_VALUE}'
```
<br>

<h1 align="left">Usage</h1>

<h2 align="left">Reader</h2>

```py
from TCGCSUtils import GCSReader

reader = GCSReader()

# Read from JSON
dataframe = reader.read_from_json(
    bucket_name, # Bucket name
    prefix, # Path prefix like path/to/folder
    max_results, # Max of results
    return_dataframe, # True or False
    delta_time_kwargs # A dictonary with times to remove from now, for example:
    # {"hour": 1} - You're saying you want files from an hour ago.
    # You can pass hour, minute, seconds or days.
)

# Read from parquet
dataframe = reader.read_from_parquet(
    bucket_name, # Bucket name
    prefix, # Path prefix like path/to/folder
    max_results # Max of results,
    delta_time_kwargs # A dictonary with times to remove from now, for example:
    # {"hour": 1} - You're saying you want files from an hour ago.
    # You can pass hour, minute, seconds or days.
)
```

<h2 align="left">Writer</h2>

```py
from TCGCSUtils import GCSWriter

writer = GCSWriter()

# Write to JSON
writer.write_json(
    data, # Dictionary or List
    bucket_name, # Bucket name
    prefix, # Path prefix like path/to/folder
    file_name, # File name with extension ex. 'filename.json'
)

# Write to parquet
writer.write_parquet(
    data, # Pandas dataframe
    bucket_name, # Bucket name
    prefix, # Path prefix like path/to/folder
    file_name, # File name with extension ex. 'filename.parquet'
)
```