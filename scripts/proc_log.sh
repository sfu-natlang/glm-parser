mv $1 $1.bak
awk '/[DEBUG]|[INFO]|[WARN]/'  $1.bak > $1

sed -i.bak '/ LEARNER [INFO] Iteration:/d' $1
sed -i.bak '/ EVALUATOR [INFO] Sentence/d' $1

sed -i.bak '/ [DEBUG]: Time usage/d' $1
sed -i.bak '/ [DEBUG]: Data finishing/d' $1
sed -i.bak '/ [DEBUG]: Loading data/d'	$1
sed -i.bak '/ [DEBUG]: data instance/d' $1
sed -i.bak '/ [DEBUG]: \[/d' $1
sed -i.bak '/ [DEBUG]: result edge/d' $1

sed -i.bak '/ [DEBUG]: gold edge/d' $1
sed -i.bak '/ [DEBUG]: set/d' $1
sed -i.bak '/ [DEBUG]: Correct_num/d' $1
sed -i.bak '/ [DEBUG]: ######/d' $1

sed -i.bak '/ [DEBUG]: Command to send:/d' $1
sed -i.bak '/ [DEBUG]: Answer received:/d' $1
sed -i.bak '/ [DEBUG]: JavaGateway/d' $1
