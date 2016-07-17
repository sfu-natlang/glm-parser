mv $1 $1.bak
awk '/\[DEBUG\]|\[INFO\]|\[WARN\]/'  $1.bak > $1

sed -i.bak '/ LEARNER \[INFO\]: Iteration/d' $1
sed -i.bak '/ EVALUATOR \[INFO\]: Sentence/d' $1
sed -i.bak '/ EVALUATOR \[DEBUG\]: /d' $1
