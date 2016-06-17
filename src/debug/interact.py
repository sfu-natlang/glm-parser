#
# Global Linear Model Parser
# Simon Fraser University
# NLP Lab
#
# Author: Yulan Huang, Ziqi Wang, Anoop Sarkar
# (Please add on your name if you have authored this file)
#

import parse.ceisner
import parse.ceisner3

from data.data_pool import *
from learn.perceptron import *

from learn.average_perceptron import AveragePerceptronLearner
from learn.perceptron import PerceptronLearner

from evaluate.evaluator import *

from weight.weight_vector import *
import debug
import sys
import getopt
import readline
import time

first_time = True


def get_prompt(name_stack):
    p = name_stack[0]
    for i in name_stack[1:]:
        p += '.i'
    return "[%s]>>>" % (p, )


def print_attr(argv, locals_dict):
    opt_spec = "l"
    opts, args = getopt.getopt(argv[1:], opt_spec)
    for obj_name in args:
        current_obj = locals_dict[obj_name]
        for attr_name in current_obj.__dict__:
            if ('-l', '') not in opts:
                sys.stdout.write(attr_name + ' ')
            else:
                sys.stdout.write("%s\t\t%s\n" % (attr_name,
                                                 str(type(getattr(current_obj, attr_name)))))
        print("\n")
    return


def interact(root_obj, root_name, position,
             globals_dict, locals_dict):
        """
        Interact with user
        """
        global first_time

        if first_time is True:
            print("*************************************")
            print("* Welcome to interactive glm-parser *")
            print("*************************************")
            first_time = False

        print(position)

        obj_stack = [root_obj]
        name_stack = [root_name]
        while True:
            s = raw_input(get_prompt(name_stack))
            s = s.strip()
            if s == '':
                continue

            s_list = s.split()

            op = s_list[0]

            if op == "continue":
                break
            elif op == 'exit':
                sys.exit(1)
            elif op == 'attr':
                print_attr(s_list, locals_dict)
            else:
                command = ''
                for i in s_list:
                    command += (i + ' ')
                print('Python interpreter: %s' % (command, ))

                try:
                    exec(command, globals_dict, locals_dict)
                except Exception as e:
                    print(e)

        return

#####################################################

def data_pool_get_data_list_wrapper(self, file_path):
        """
        Form the DependencyTree list from the specified file. The file format
        is defined below:

        ----------------------------------------------
        [previous sentence]
        [empty line]
        {word} {pos} {parent index} {edge_property}
        ...
        ...
        [empty line]
        [next sentence]
        ----------------------------------------------

        * Sentences are separated by an empty line
        * Each entry in the sentence has an implicit index

        :param file_path: the path to the data file
        :type file_path: str

        :return: a list of DependencyTree in the specified file
        :rtype: list(Sentence)
        """
        f = open(file_path)

        data_list = []
        word_list = []
        pos_list = []
        edge_set = {}
        current_index = 0

        sent_count = 0

        print(file_path)

        for line in f:
            line = line[:-1]
            if line != '':
                current_index += 1
                entity = line.split()
                if len(entity) != 4:
                    logging.error("Invalid data format - Length not equal to 4")
                else:
                    # We do not add the 'ROOT' for word and pos
                    # They are added in class Sentence
                    word_list.append(entity[0])
                    pos_list.append(entity[1])
                    edge_set[(int(entity[2]), current_index)] = entity[3]
            else:
                # Prevent any non-mature (i.e. trivial) sentence structure
                if word_list != []:
                    # Add "ROOT" for word and pos here
                    sent = Sentence(word_list,pos_list,edge_set)
                    sent_count += 1
                    data_list.append(sent)
                    sys.stdout.write("*** [info] Load sentence %d\r" % (sent_count, ))

                word_list = []
                pos_list = []
                edge_set = {}
                current_index = 0

        # DO NOT FORGET THIS!!!!!!!!!!!!
        f.close()
        print("")

        return data_list

#####################################################

       
def glm_parser_sequential_train_wrapper(self, train_section=[], max_iter=-1, d_filename=None):
    if not train_section == []:
        train_data_pool = DataPool(train_section, self.data_path)
        # Interactive
        interact(train_data_pool, "train_data_pool", "*** [info] Finished loading training section",
                 globals(), locals())
    else:
        train_data_pool = self.train_data_pool
            
    if max_iter == -1:
        max_iter = self.max_iter
            
    self.learner.sequential_learn(self.compute_argmax, train_data_pool, max_iter, d_filename)
    
def glm_parser_evaluate_wrapper(self, test_section=[]):
    if not test_section == []:
        test_data_pool = DataPool(test_section, self.data_path)
    else:
        test_data_pool = self.test_data_pool

    self.evaluator.evaluate(test_data_pool, self.parser, self.w_vector)
        
def glm_parser_compute_argmax_wrapper(self, sentence):
    current_edge_set = self.parser.parse(sentence, self.w_vector.get_vector_score)
    current_global_vector = sentence.get_global_vector(current_edge_set)

    return current_global_vector

#########################################################################

def average_perceptron_learner_sequential_learn_wrapper(self, f_argmax, data_pool=None, max_iter=-1, d_filename=None):
    if max_iter <= 0:
        max_iter = self.max_iter

    logging.debug("Starting sequential train ... ")

    # sigma_s
    self.weight_sum_dict.clear()
    self.last_change_dict.clear()
    self.c = 1

    # for t = 1 ... T
    for t in range(max_iter):
        logging.debug("Iteration: %d" % t)
        logging.debug("Data size: %d" % len(data_pool.data_list))
        sentence_count = 1
        argmax_time_total = 0.0
        # for i = 1 ... m
        while data_pool.has_next_data():
            print("Sentence %d" % (sentence_count, ))
            sentence_count += 1
            # Calculate yi' = argmax
            data_instance = data_pool.get_next_data()
            gold_global_vector = data_instance.gold_global_vector

            if debug.time_accounting_flag is True:
                before_time = time.clock()
                current_global_vector = f_argmax(data_instance)
                after_time = time.clock()
                time_usage = after_time - before_time
                argmax_time_total += time_usage
                print("Time usage: %f" % (time_usage, ))
                logging.debug("Time usage %f" % (time_usage, ))
            else:
                # Just run the procedure without any interference
                current_global_vector = f_argmax(data_instance)

            delta_global_vector = gold_global_vector - current_global_vector

            interact(current_global_vector, "current_global_vector",
                     "*** [info] Finished argmax-ing one sentence",
                     globals(), locals())

            # update every iteration (more convenient for dump)
            if data_pool.has_next_data():
                # i yi' != yi
                if not current_global_vector == gold_global_vector:
                    # for each element s in delta_global_vector
                    for s in delta_global_vector.keys():
                        self.weight_sum_dict[s] += self.w_vector[s] * (self.c - self.last_change_dict[s])
                        self.last_change_dict[s] = self.c

                    # update weight and weight sum
                    self.w_vector.iadd(delta_global_vector.feature_dict)
                    self.weight_sum_dict.iadd(delta_global_vector.feature_dict)

            else:
                for s in self.last_change_dict.keys():
                    self.weight_sum_dict[s] += self.w_vector[s] * (self.c - self.last_change_dict[s])
                    self.last_change_dict[s] = self.c

                if not current_global_vector == gold_global_vector:
                    self.w_vector.iadd(delta_global_vector.feature_dict)
                    self.weight_sum_dict.iadd(delta_global_vector.feature_dict)

            self.c += 1

            # If exceeds the value set in debug config file, just stop and exit
            # immediately
            if sentence_count > debug.run_first_num > 0:
                print("Average time for each sentence: %f" % (argmax_time_total / debug.run_first_num))
                logging.debug(
                    "Average time for each sentence: %f" % (argmax_time_total / debug.run_first_num))
                sys.exit(1)

        # End while(data_pool.has_next_data())

        # Reset index, while keeping the content intact
        data_pool.reset_index()

        if d_filename is not None:
            p_fork = multiprocessing.Process(
                target=self.dump_vector,
                args=(d_filename, t))

            p_fork.start()
            # self.w_vector.dump(d_filename + "_Iter_%d.db"%t)

    self.w_vector.clear()

    self.avg_weight(self.w_vector, self.c - 1)

    return

