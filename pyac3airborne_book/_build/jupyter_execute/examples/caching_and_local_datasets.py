# Caching and local datasets
Datasets accessed via the intake catalog can be either downloaded into a temporary folder, from where they will be deleted after restarting python, or permanently into a specified directory. If the dataset is already contained within the specified directory, intake will load the data from the local source, instead of downloading it again from the remote server. This is recommended for large datasets or datasets which are used regularily.

The following example shows, how to supply local directories to intake using the `simplecache` functionality. Directories of many local datasets are suggested to be stored in a single `.yaml` file to avoid the specification of local directories within the python routines.

## Loading the intake catalog
We load the intake catalog from ac3airborne, which contains paths to the remote servers, where files are stored.

import ac3airborne

cat = ac3airborne.get_intake_catalog()

## Example: Dropsonde data
The caching functionality will be demonstrated with the dropsonde data published online on the PANGAEA data base. The file of the dataset on PANGAEA is contained in the intake catalog.

### Option 1: Download into temporary folder
The download into the temporary folder is the default behaviour. Usually the dataset is stored in the `/tmp` directory.

ds_dsd = cat['P5']['DROPSONDES']['ACLOUD_P5_RF23'](i_sonde=1).to_dask()

By default, the variable name is not readable. By setting the parameter `same_names` of the `simplecache` group to *True* and supplying it to the `storage_options` parameter, the downloaded file has the same file name as the remote file (i.e. the file on PANGAEA).

kwds = {'simplecache': dict(
    same_names=True
)}

ds_dsd = cat['P5']['DROPSONDES']['ACLOUD_P5_RF23'](i_sonde=1, storage_options=kwds).to_dask()

### Option 2: Permanent download into local directory
Under the `storage_options` parameter, we can also specify the local directory of the dataset. The path will be supplied to the `same_names` parameter of the `simplecache` group as shown below. If the remote file is contained in the local directory, the local file will be read. Else, the remote file will be downloaded and stored at the specified location permanently. The next time, the data is imported, intake will use the local file. 

Here, we will store the data relative to the current working directory at `./data/dropsondes`.

kwds = {'simplecache': dict(
    cache_storage='./data/dropsondes', 
    same_names=True
)}

ds_dsd = cat['P5']['DROPSONDES']['ACLOUD_P5_RF23'](i_sonde=1, storage_options=kwds).to_dask()

## Managing directories of multiple datasets
Datasets may be stored locally in different directories. Instead of specifying the directory in every python script, we can use one file, where all paths are stored for each dataset. Here, we will use a `yaml` file, as it can be read easily into a python dictionary.

The file may be structured like this:
```
DROPSONDES: '/local/path/to/dropsondes'
BROADBAND_IRRADIANCE: '/local/path/to/broadband_irradiance'
FISH_EYE: '/local/path/to/fish_eye'
```

In the following, the data will be downloaded in or used from the local *./data* folder of the current working directory.

import yaml

Now we read the pre-defined yaml file

with open('./local_datasets.yaml', 'r') as f:
    local_dir = yaml.safe_load(f)
print(local_dir)

As a test, we will download the dropsonde data from ACLOUD RF05.

dataset = 'DROPSONDES'
flight_id = 'ACLOUD_P5_RF05'

We can access the directory, where the data is stored using the dataset name.

print(local_dir[dataset])

We add the path now to the `storage_options` parameter.

kwds = {'simplecache': dict(
    cache_storage=local_dir[dataset], 
    same_names=True
)}

Now we download or use the local dropsonde file. Afterwards, check if the directory `.data/dropsondes` was created and contains the file `DS_ACLOUD_Flight_05_20170525_V2.nc`. If the directory and the file already exist, the local file will be read.

ds = cat.P5[dataset][flight_id](i_sonde=1, storage_options=kwds).to_dask()