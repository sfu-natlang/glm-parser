# -*- coding: utf-8 -*-
import feature_set, dependency_tree
# sample cmd:
# python feature_set_merge.py "sec_2_iter_0.db" "sec_3_iter_0.db" "merged.db"
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print "please provide the name of the two db files and the output file name"
        sys.exit(1)
    
    db_1 = sys.argv[1]
    db_2 = sys.argv[2]
    output_file = sys.argv[3]

    dt = dependency_tree.DependencyTree()
    
    fset_1 = feature_set.FeatureSet(dt,operating_mode='memory_dict')
    fset_2 = feature_set.FeatureSet(dt,operating_mode='memory_dict')

    fset_1.load(db_1)
    fset_2.load(db_2)

    fset_1.merge(fset_2)
    fset_1.dump(output_file)
