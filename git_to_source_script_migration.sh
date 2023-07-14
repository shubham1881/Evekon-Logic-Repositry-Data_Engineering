if [ -z "$1" ]
  then
    echo "No argument provided"
    exit 1
fi

while getopts i:o: flag
do
case "${flag}" in
i) source=${OPTARG};;
o) target=${OPTARG};;
esac
done
echo "source_path: $source"
echo "target_path: $target"



if [ -z "$source" ]
then
echo "Github path not entered. Please enter github path."
exit 1
fi

if [ -z "$target" ]
then
echo "Target path not present."
echo "Exiting the script"
exit 1
fi

cur_date=`date +%Y-%m-%d`
echo "Executing Script for date $cur_date"
file=$(basename $source)
echo "File name: $file"
extension=${file##*.}
echo "Extension of the file: $extension"

substr="github_path"

if [[ $source == *"$substr"* ]]
then
echo "File is from GIT DEV branch. Proceeding Further"
else
echo "File is not from GIT DEV branch. Please check source path"
echo "Exiting the script"
exit 1
fi

if [[ $extension == "py" || $extension == "sh" || $extension == "json" ]]
        then
        echo "starting download for $file"
	(cd $target && curl --header "Authorization: token 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" --header 'Accept: application/vnd.github.v3.raw' --remote-name --location $source)
	echo "Download completed for $file"
        else
        echo "$file is directory or extension is different. $file cannot be downloaded. Please check Path"
        fi
