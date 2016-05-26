#usage: proc_log.sh LOGFILE
sed -i.bak '/DEBUG: Time usage/d' $1
sed -i.bak '/DEBUG: Data finishing/d' $1
sed -i.bak '/DEBUG: Loading data/d'	$1
sed -i.bak '/DEBUG: data instance/d' $1
sed -i.bak '/DEBUG: \[/d' $1
sed -i.bak '/DEBUG: result edge/d' $1

sed -i.bak '/DEBUG: gold edge/d' $1
sed -i.bak '/DEBUG: set/d' $1
sed -i.bak '/DEBUG: Correct_num/d' $1
sed -i.bak '/DEBUG: ######/d' $1
