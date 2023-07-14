cur_date=`date +%y-%m-%d`
echo $cur_date
folder_path="/usr/lib/airflow/logs/scheduler/"
echo "Clearing Airflow logs from $folder_path older than 7 days"
date_before_rdt=`date -d "$cur_date 7 days ago" +%Y-%m-%d`
echo $date_before_rdt
older_files=`find $folder_path ! -newermt $date_before_rdt`
for file in $older_files
        do
        if [[ -d $file ]]
        then
        echo "$file is a directory and marked for remove"
        rm -rf $file
        echo "$file removed sucessfully"
        else
#        echo "listing file :: $file no need to delete"
        echo $file
        fi
        done
