#!/usr/bin/env bash

set -e

pipeline_directory=$PIPELINE_DIRECTORY
data_source="seconds.csv"
output_file="male.csv"

echo "Splitting out Male Cat Data"
# where column == sleep_duration_minutes, convert to seconds
IFS=',' read -r -a array <<< "$(head -n 1 ${pipeline_directory}/${data_source})"
for index in "${!array[@]}"
do
    if   [ ${array[index]} = 'gender' ]; then
        gender=$((index+1))
        echo -n 'gender,' >> ${pipeline_directory}/${output_file}

    elif [ ${array[index]} = 'sleep_duration_seconds' ]; then
        duration=$((index+1))
        echo -n 'sleep_duration_seconds,' >> ${pipeline_directory}/${output_file}

    fi
done
echo '' >> ${pipeline_directory}/${output_file}

echo "Writing Male Cat Data to male.csv"
# write the columns we want to file
cat ${pipeline_directory}/${data_source} | tail -n +2 | while read line 

do
    if  [[ $(echo $line | cut -d',' -f$gender) = 'Male' ]]; then
        value_duration=$(echo $line | cut -d',' -f$duration)
        echo Male,$value_duration >> ${pipeline_directory}/${output_file}
    fi
done
