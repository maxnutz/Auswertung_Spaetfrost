"""
creates dataset with number of frost days for input files
- needs write and create permissions in input-folder
- writes outputfile into inputfolder
- needs python environment environment.yml
- inputfolder: folder holding only the input-files! 
"""

import xarray as xr
import os


def get_all_inputfiles(folder_path):
    if not os.path.exists(folder_path):
        raise ValueError(f"The folder '{folder_path}' does not exist.")

    if not os.path.isdir(folder_path):
        raise ValueError(f"The path '{folder_path}' is not a folder.")

    file_paths = [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, file))
    ]
    return file_paths


# get list of inputfiles
inputfolder = "/home/max/Dokumente/Skripts/Auswertung_Spaetfrost/Files_input/"
outputfolder = (
    "/home/max/Dokumente/Skripts/Auswertung_Spaetfrost/Files_input/outputfolder/"
)
inputfiles = get_all_inputfiles(inputfolder)  # TODO to define
outputfiles = [
    outputfolder + file.split("/")[-1][:-3] + "_critical_frostdays.nc"
    for file in inputfiles
]


# define periode to process
start_day = 90
end_day = 110

for file, outputfile in zip(inputfiles, outputfiles):
    try:
        print("Import file " + file)
        ds = xr.open_dataset(file)
        doy_ds = ds["time"].dt.dayofyear
        ds_filtered = ds.where((doy_ds >= start_day) & (doy_ds <= end_day), drop=True)
    except Exception as e:
        print(
            ">>> Error while opening file '"
            + file
            + "'. Skipping this file. \nError: "
            + str(e)
        )
    else:
        print("Process file " + file)
        ds_frostday = ds_filtered["TN"].where(ds_filtered["TN"] < 0, 1)
        ds_frostday = ds_frostday.where(ds_frostday > 0, 0)
        count_frostdays = ds_frostday.sum(dim="time", skipna=True)
        ds_frostdays = count_frostdays.to_dataset(name="critical_frostdays")
        ds_frostdays.to_netcdf(outputfile)
