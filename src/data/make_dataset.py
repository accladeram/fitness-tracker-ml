import pandas as pd
from glob import glob
from pathlib import Path

# --------------------------------------------------------------
# Read single CSV file
# --------------------------------------------------------------
single_file_acc = pd.read_csv(
    "../../data/raw/MetaMotion/A-bench-heavy_MetaWear_2019-01-14T14.22.49.165_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv"
)

single_file_gyr = pd.read_csv(
    "../../data/raw/MetaMotion/A-bench-heavy2_MetaWear_2019-01-14T14.27.00.784_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv"
)

# --------------------------------------------------------------
# List all data in data/raw/MetaMotion
# --------------------------------------------------------------
path = Path("../../data/raw/MetaMotion")
files = [str(f) for f in path.glob("*.csv")]
# --------------------------------------------------------------
# Extract features from filename
# --------------------------------------------------------------
root_path = "..\\..\\data\\raw\\MetaMotion\\"
file_path = files[0]

participant = file_path.split("-")[0].replace(root_path, "")
label = file_path.split("-")[1]
category = file_path.split("-")[2].rstrip(
    "123"
)  # rstrip removes any trailing (ending) characters, spaceis the default

df = pd.read_csv(file_path)
df["participant"] = participant
df["label"] = label
df["category"] = category


# --------------------------------------------------------------
# Read all files
# --------------------------------------------------------------
acc_df = pd.DataFrame()
gyr_df = pd.DataFrame()

acc_set=1
gyr_set=1

for file in files:
    
    participant = file.split("-")[0].replace(root_path, "")
    label = file.split("-")[1]
    category = file.split("-")[2].rstrip(
    "123456789_MetaWear_0123456789") 
    df = pd.read_csv(file)
    df["participant"] = participant
    df["label"] = label
    df["category"] = category
    if "Accelerometer" in file:
        df["set"] = acc_set
        acc_set += 1
        acc_df = pd.concat([acc_df, df], ignore_index=True)
        
    if "Gyroscope" in file:
        df["set"] = gyr_set
        gyr_set += 1
        gyr_df = pd.concat([gyr_df, df], ignore_index=True)
        
# --------------------------------------------------------------
# Working with datetimes
# --------------------------------------------------------------
df.info()
# Convert epoch (ms) to datetime
pd.to_datetime(df["epoch (ms)"], unit="ms", utc=True)

acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms", utc=True)
gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms", utc=True)

#remove columns
del acc_df["epoch (ms)"]
del acc_df["time (01:00)"]
del acc_df["elapsed (s)"]

del gyr_df["epoch (ms)"]
del gyr_df["time (01:00)"]  
del gyr_df["elapsed (s)"]


# --------------------------------------------------------------
# Turn into function
# --------------------------------------------------------------
path = Path("../../data/raw/MetaMotion")
files = [str(f) for f in path.glob("*.csv")]
root_path = "..\\..\\data\\raw\\MetaMotion\\"

def read_and_process_files(files, root_path):
    acc_df = pd.DataFrame()
    gyr_df = pd.DataFrame()

    acc_set=1
    gyr_set=1

    for file in files:
        
        participant = file.split("-")[0].replace(root_path, "")
        label = file.split("-")[1]
        category = file.split("-")[2].rstrip(
        "123456789_MetaWear_0123456789") 
        df = pd.read_csv(file)
        df["participant"] = participant
        df["label"] = label
        df["category"] = category
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

    #remove columns
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


# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz


# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------
