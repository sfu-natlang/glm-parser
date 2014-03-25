import data_set, feature_set, dependency_tree
import weight_learner, evaluator, glm_parser

def write_file(msg):
    f = open(output_file, "a+")
    f.write(msg)
    f.close()
    return


if __name__ == "__main__":
    import sys
    test_secs = [0,1,22,24]
   
    begin_sec = 2
    end_sec = 21

    iteration = 0 #int(sys.argv[2])
    trainsection = [(2,21)]#int(sys.argv[1])

    output_file = "./train.out"
    max_iteration = 200
    #pre_iteration = iteration-1

    test_data_path = "/cs/natlang-projects/glm-parser/penn-wsj-deps/"
    #db_path = "/cs/natlang-projects/glm-parser/results/"
    #db_name = "train_iter_%d_sec_%d"

    #dt = dependency_tree.DependencyTree()

    #fset_1 = feature_set.FeatureSet(dt, operating_mode='memory_dict')
    #fset_1.load(db_path + db_name%(pre_iteration, end_sec) + ".db")
    #for i in range(begin_sec, end_sec):
        #fset_2 = feature_set.FeatureSet(dt,operating_mode='memory_dict')
        #fset_2.load(db_path + db_name%(pre_iteration, i) + ".db")
        #print "fs2 " + db_name % (pre_iteration, i) + " load successfully"

        #fset_1.merge(fset_2)
        #print "merge done"

        #del fset_2

    gp = glm_parser.GlmParser()
    #gp.set_feature_set(fset_1)
    
    #output_file = db_path + db_name % (iteration, trainsection)
    #print output_file, trainsection
    for iteration in range(max_iteration):
        write_file("***************************************************\n")
        write_file("Iteration %d: \n    Start training...\n" % iteration)
        fset = gp.train(trainsection, test_data_path, dump=False)
        write_file("    Training done!!!\n")

        write_file("    Calculating accuracy...\n")
        for s in test_secs:
            acc = gp.unlabeled_accuracy(section_set=[s],data_path=test_data_path)
            stats = gp.get_evaluator().get_statistics()
            write_file("    Section %d -- Accuracy: %lf"%(s,acc) + "  ( %d / %d ) \n"%stats )
    

    #print output_file + " done "

