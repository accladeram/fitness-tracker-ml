import pandas as pd
from glob import glob
from pathlib import Path

# --------------------------------------------------------------
# Turn into function
# --------------------------------------------------------------
path = Path("../../data/raw/MetaMotion")
files = [str(f) for f in path.glob("*.csv")]
root_path = "..\\..\\data\\raw\\MetaMotion\\"


def read_and_process_files(files, root_path):
    acc_df = pd.DataFrame()
    gyr_df = pd.DataFrame()

    acc_set = 1
    gyr_set = 1

    for file in files:
        participant = file.split("-")[0].replace(root_path, "")
        label = file.split("-")[1]
        category = file.split("-")[2].rstrip("123456789_MetaWear_0123456789")
        df = pd.read_csv(file)
        df["label"] = label
        df["category"] = category
        df["participant"] = participant

        if "Accelerometer" in file:
            df["set"] = acc_set
            acc_set += 1
            acc_df = pd.concat([acc_df, df], ignore_index=True)

        if "Gyroscope" in file:
            df["set"] = gyr_set
            gyr_set += 1
            gyr_df = pd.concat([gyr_df, df], ignore_index=True)
    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms", utc=True)
    gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms", utc=True)

    # remove columns
    del acc_df["epoch (ms)"]
    del acc_df["time (01:00)"]
    del acc_df["elapsed (s)"]
    del gyr_df["epoch (ms)"]
    del gyr_df["time (01:00)"]
    del gyr_df["elapsed (s)"]
    return acc_df, gyr_df


acc_df, gyr_df = read_and_process_files(files, root_path)


# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------
data_merge = pd.concat(
    [acc_df.iloc[:, :3], gyr_df], axis=1
)  # combine along columns, acc_df takes first 3 columns,because they are include in gyr_df

data_merge.columns = [
    "acc_x",
    "acc_y",
    "acc_z",
    "gyr_x",
    "gyr_y",
    "gyr_z",
    "label",
    "category",
    "participant",
    "set",
]

# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz
# sync up the two sensors frequency
# resample function with rule, it is important to specify index as time series when resampling with rules

# we will not use Seconds as rule, because we could lose data
# data_merge.resample(rule="S").mean()

# we will not use Mean aggregation, because we use categorical data
# data_merge = data_merge.resample(rule="200ms").mean()

# we will use a custom aggregation function with apply method
sampling = {
    "acc_y": "mean",
    "acc_x": "mean",
    "acc_z": "mean",
    "gyr_x": "mean",
    "gyr_y": "mean",
    "gyr_z": "mean",
    "label": "last",
    "category": "last",
    "participant": "last",
    "set": "last",
}

# resample looks at the first and last daytime index, and fill the gaps in between with a frequency as defined by rule for the whole period. even if there is no data for a specific time point,it will create a new row
# data_merge[:].resample(rule="200ms").apply(sampling)

# Split df into data frames for separate days
days_df = [g for n, g in data_merge.groupby(pd.Grouper(freq="D"))]

data_resampled = pd.concat([df.resample(rule="200ms").apply(sampling).dropna() for df in days_df])

data_resampled["set"] = data_resampled["set"].astype("int")

data_resampled.info()

# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------

# picke method is used to export the dataset in a serialized format, then when loading the dataset, it will be in the same format as it was before. useful when working with timestamps and indexes that change, we won't have to make the conversion again
data_resampled.to_pickle("../../data/interim/01_data_processed.pkl")

#pickle file is a binary file, it is not human readable. They are smaller than csv files and faster to read and write, we don't have to worry about the data types, convertions, they are preserved in the pickle file.
#https://www.geeksforgeeks.org/python/understanding-python-pickling-example/





