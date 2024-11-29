"""
creates dataset with number of frost days for input files
- needs write and create permissions in input-folder
- writes outputfile into inputfolder
- needs python environment environment.yml
- inputfolder: folder holding only the input-files! 
"""

import xarray as xr
import pandas as pd
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


def process_temperature_files(inputfiles, outputfiles, start_day, end_day):
    """Calculates frost days from TN-Input"""
    list_frostdays_per_year = []
    list_timesteps = []
    for file, outputfile in zip(inputfiles, outputfiles):
        try:
            print("Import file " + file)
            ds = xr.open_dataset(file)
            doy_ds = ds["time"].dt.dayofyear
            ds_filtered = ds.where(
                (doy_ds >= start_day) & (doy_ds <= end_day), drop=True
            )
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
            print("Saved output to file " + outputfile)
        finally:
            print("Start meaning for  file " + file + "\n")
        try:
            number_frostdays = (
                ds_frostdays["critical_frostdays"]
                .mean(dim=["x", "y"], skipna=True)
                .values
            )
            list_timesteps.append(ds_frostday.time[0].values)
            list_frostdays_per_year.append(number_frostdays)
        except Exception as e:
            print(
                (
                    ">>> Error while calculating mean. Output Rasterfile saved. Error:\n "
                    + str(e)
                )
            )
    return list_timesteps, list_frostdays_per_year


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

# make folderstructure
if not os.path.exists(outputfolder):
    os.mkdir(outputfolder + "/temp/")


# define periode to process and corresponding output_folder
start_day_first_period = 90
end_day_first_period = 110
outputfiles_first_period = [
    outputfolder
    + "/temp/"
    + file.split("/")[-1][:-3]
    + "_critical_frostdays_first_period.nc"
    for file in inputfiles
]

start_day_second_period = 100
end_day_second_period = 120
outputfiles_first_period = [
    outputfolder
    + "/temp/"
    + file.split("/")[-1][:-3]
    + "_critical_frostdays_second_period.nc"
    for file in inputfiles
]


# caluculate frost days raster
print("\nCALCULATION OF FIRST PERIOD")
first_timesteps, first_frostdays = process_temperature_files(
    inputfiles, outputfiles, start_day_first_period, end_day_first_period
)
print("\nCALCULATION OF SECOND PERIOD")
second_timesteps, second_frostdays = process_temperature_files(
    inputfiles, outputfiles, start_day_second_period, end_day_second_period
)

if len(first_timesteps) == len(second_timesteps):
    df = pd.DataFrame(
        index=first_timesteps,
        columns=[
            "critical_frostdays period 90 110",
            "critical_frostdays period 100 120",
        ],
    )
    df["critical_frostdays period 90 110"] = first_frostdays
    df["critical_frostdays period 100 120"] = second_frostdays
    df.to_csv(outputfolder + "frostdays.csv")
else:
    raise RuntimeError(
        "Number of Timesteps should be equal but lists length differ. STOPPING "
    )
os.rmdir(outputfolder + "/temp/")
