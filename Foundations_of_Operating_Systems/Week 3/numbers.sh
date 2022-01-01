START_TIME=$SECONDS
for i in {1..1000000}
do
    echo $RANDOM >> file1.txt
done
ELAPSED_TIME=$(($SECONDS - $START_TIME))
echo "$ELAPSED_TIME seconds"