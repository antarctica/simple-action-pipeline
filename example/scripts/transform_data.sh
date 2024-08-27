#!/usr/bin/env bash

set -e

pipeline_directory=$PIPELINE_DIRECTORY
data_source="columns.csv"

echo "Converting SleepyTime minutes to seconds"
# where column == sleep_duration_minutes, convert to seconds
IFS=',' read -r -a array <<< "$(head -n 1 ${pipeline_directory}/$data_source)"
for index in "${!array[@]}"
do
    if   [ ${array[index]} = 'gender' ]; then
        gender=$((index+1))
        echo -n 'gender,' >> ${pipeline_directory}/seconds.csv

    elif [ ${array[index]} = 'sleep_duration_minutes' ]; then
        duration=$((index+1))
        echo -n 'sleep_duration_seconds,' >> ${pipeline_directory}/seconds.csv

    fi
done
echo '' >> ${pipeline_directory}/seconds.csv

echo "Writing converted columns to seconds.csv"
# write the columns we want to file
cat ${pipeline_directory}/columns.csv | tail -n +2 | while read line 
do
    value_gender=$(echo $line | cut -d',' -f$gender)
    value_duration=$(echo $line | cut -d',' -f$duration)
    value_duration=$(echo $value_duration " * 60" | bc )
    echo $value_gender,$value_duration >> ${pipeline_directory}/seconds.csv
done

echo "Removing columns file"
rm ${pipeline_directory}/columns.csv
