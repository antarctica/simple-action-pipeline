#!/usr/bin/env bash

set -e

pipeline_directory=$PIPELINE_DIRECTORY
data_source="../assets/data/cat_sleepytime_duration_data.csv"

echo "Reading Cat SleepyTime Duration data"
cp ${pipeline_directory}/${data_source} ${pipeline_directory}/data_file.csv

echo "Extracting columns"
# extract column numbers for 'gender' and 'sleep_duration_minutes'
IFS=',' read -r -a array <<< "$(head -n 1 data_file.csv)"
for index in "${!array[@]}"
do
    if   [ ${array[index]} = 'gender' ]; then
        gender=$((index+1))

    elif [ ${array[index]} = 'sleep_duration_minutes' ]; then
        duration=$((index+1))

    fi
done

echo "Writing extracted columns to columns.csv"
# write the columns we want to file
cat data_file.csv | cut -d',' -f$gender,$duration >> ${pipeline_directory}/columns.csv

echo "Removing original file"
rm ${pipeline_directory}/data_file.csv
