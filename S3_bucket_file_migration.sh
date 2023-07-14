#file without latest date
echo "starting copy of file"
aws s3 cp source_path TARGET_PATH_s3
echo "completed copy of file"

#file according to latest
echo "starting copy of file"
SOURCE="file path"
ebs_mfr_export_file=`aws s3 ls $SOURCE  | sort | grep -i "file name" |tail -n 1 | awk '{print $4}'`
SOURCE_PATH="${SOURCE}${ebs_mfr_export_file}"
echo $SOURCE_PATH
TARGET_PATH="target path"
echo $TARGET_PATH
aws s3 cp $SOURCE_PATH $TARGET_PATH
echo "completed copy of file"