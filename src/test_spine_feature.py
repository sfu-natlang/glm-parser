from spineparse.parser_feature_generator import ParserFeatureGenerator
from data.data_pool import *
from feature.feature_vector import FeatureVector

if __name__ == "__main__":
    import getopt, sys
    
    data_path = "/cs/natlang-projects/glm-parser/new_results/wsj_conll_tree/lossy/"
    select_section = [0]
    data_pool = DataPool(select_section, data_path)
    data_instance = data_pool.get_next_data()
    psent = ParserFeatureGenerator(data_instance)
    edge_list = data_instance.get_edge_list()

    global_vector = FeatureVector()
    for head,mod in edge_set:
        h_spine = psent.spine_list[head]
        join_number = h_spine.count('(')
        for join_pos in range(join_number):
            for r_or_s in range(2):
                local_vector = psent.get_local_vector(head, modifier, join_pos+1, r_or_s)
                global_vector.aggregate(local_vector)
                
    filename = "spinefeature.log"
    fp = open(filename,"w")
    for key in global_vector.keys():
        fp.write(key + "\n")

