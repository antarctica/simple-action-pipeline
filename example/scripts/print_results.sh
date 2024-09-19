#!/usr/bin/env bash

#Script to take the results from the example and print them
#to std output and a log file.

set -e

pipeline_directory=$PIPELINE_DIRECTORY
data_source1="female.csv"
data_source2="male.csv"
output_file="results.log"

#echo "Removing old seconds.csv file"
#rm ${pipeline_directory}/seconds.csv

echo 'Cat SleepyTime Results' > ${pipeline_directory}/${output_file}
echo '======================' >> ${pipeline_directory}/${output_file}

echo "Generating Results"
# for female cat data
IFS=',' read -r -a array <<< "$(head -n 1 ${pipeline_directory}/${data_source1})"
for index in "${!array[@]}"
do
    if   [ ${array[index]} = 'gender' ]; then
        gender=$((index+1))

    elif [ ${array[index]} = 'sleep_duration_seconds' ]; then
        duration=$((index+1))

    fi
done

echo "Processing Female Cat Data"
# get values for female cats

cat_count=0
dur_min=999999
dur_max=0.0
dur_total=0.0
end_loop=$(cat ${pipeline_directory}/${data_source1} | tail -n +2 | wc -l)


cat ${pipeline_directory}/${data_source1} | tail -n +2 | while read line 

do
    cat_count=$((cat_count+1))
    if    [[ $(bc <<< "$(echo $line | cut -d',' -f$duration) < ${dur_min}") == 1 ]]; then
        dur_min=$(echo $line | cut -d',' -f$duration)

    elif  [[ $(bc <<< "$(echo $line | cut -d',' -f$duration) > ${dur_max}") == 1 ]]; then
        dur_max=$(echo $line | cut -d',' -f$duration)

    fi
    dur_total=$(bc <<< "${dur_total} + $(echo $line | cut -d',' -f$duration)")
    
    # at the final loop iteration, output to file
    if [[ $cat_count = $end_loop ]]; then
        echo "Number of Female Cats, number  = ${cat_count}" >> ${pipeline_directory}/${output_file}
        echo "Female Min. Slept Time, secs.  = ${dur_min}" >> ${pipeline_directory}/${output_file}
        echo "Female Max. Slept Time, secs.  = ${dur_max}" >> ${pipeline_directory}/${output_file}
        echo "Total Female Sleep Time, secs. = ${dur_total}" >> ${pipeline_directory}/${output_file}
    fi

done

echo "Processing Male Cat Data"
# get values for male cats

cat_count=0
dur_min=999999
dur_max=0.0
dur_total=0.0
end_loop=$(cat ${pipeline_directory}/${data_source2} | tail -n +2 | wc -l)


cat ${pipeline_directory}/${data_source2} | tail -n +2 | while read line 

do
    cat_count=$((cat_count+1))
    if    [[ $(bc <<< "$(echo $line | cut -d',' -f$duration) < ${dur_min}") == 1 ]]; then
        dur_min=$(echo $line | cut -d',' -f$duration)

    elif  [[ $(bc <<< "$(echo $line | cut -d',' -f$duration) > ${dur_max}") == 1 ]]; then
        dur_max=$(echo $line | cut -d',' -f$duration)

    fi
    dur_total=$(bc <<< "${dur_total} + $(echo $line | cut -d',' -f$duration)")
    
    # at the final loop iteration, output to file
    if [[ $cat_count = $end_loop ]]; then
        echo "Number of Male Cats, number  = ${cat_count}" >> ${pipeline_directory}/${output_file}
        echo "Male Min. Slept Time, secs.  = ${dur_min}" >> ${pipeline_directory}/${output_file}
        echo "Male Max. Slept Time, secs.  = ${dur_max}" >> ${pipeline_directory}/${output_file}
        echo "Total Male Sleep Time, secs. = ${dur_total}" >> ${pipeline_directory}/${output_file}
    fi

done

echo "Removing source seconds.csv"
rm ${pipeline_directory}/seconds.csv
echo "Removing female and male csv files"
rm ${pipeline_directory}/${data_source1} ${pipeline_directory}/${data_source2}

echo "Printing Results"
echo
cat ${pipeline_directory}/${output_file}
