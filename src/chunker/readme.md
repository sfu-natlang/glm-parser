
# Phrasal Chunking, Homework 2

## Training phase

    python baseline.py > default.model

## Testing and Evaluation phase

    python perc.py -m default.model > output
    python score-chunks.py < output

Then upload the file `output` to the leaderboard on sfu-nlp-class.appspot.com

OR

    python perc.py -m default.model | python score-chunks.py

## Options

    python default.py -h

This shows the different options you can use in your training
algorithm implementation.  In particular the -n option will let you
run your algorithm for less or more iterations to let your code run
faster with less accuracy or slower with more accuracy. You must
implement the -n option in your code so that we are able to run
your code with different number of iterations.

