f = open('out_file.txt','r')
log = open('wrong_guesses.txt','w')
total_Ner = 0
correct_identified_Ner = 0
for line in f:
    x = line.split()
    #print (x)
    
    if not x:
        print "list is empty"
    else:
	    if x[2] != x[3]:
	        log.write("%s" %(line))
       #print "list is not empty"
       #log.write("%s\n" %(x))
#log.write("The total NER are %s\n" %(total_Ner))
#log.write("The correctly identified NER are %s\n" %(correct_identified_Ner))
f.close()
log.close()
