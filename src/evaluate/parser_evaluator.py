from __future__ import division
from pos_tagger import PosTagger
from evaluate import logger


class Evaluator():
    def __init__(self):
        self.unlabeled_correct_num = 0
        self.unlabeled_gold_set_size = 0
        return

    def __evaluate_on_datapool(data_pool, weight_vector, parser, tagger, hadoop=None):
        w_vector = WeightVector()
        for key in weight_vector.keys():
            w_vector[key] = weight_vector[key]

        unlabeled_correct_num = 0
        unlabeled_gold_set_size = 0

        sentence_count = 1
        while data_pool.has_next_data():
            sent = data_pool.get_next_data()

            if not hadoop:
                logger.info("Sentence %d of %d, Length %d" % (
                    sentence_count,
                    data_size,
                    len(sent.get_word_list()) - 1))
            sentence_count += 1

            gold_edge_set = \
                set([(head_index, dep_index) for head_index, dep_index, _ in sent.get_edge_list()])

            sent_len = len(sent.get_word_list())
            test_edge_set = \
                parser.parse(sent, w_vector.get_vector_score, tagger)

            if isinstance(test_edge_set, list):
                test_edge_set = set(test_edge_set)

            if isinstance(gold_edge_set, list):
                gold_edge_set = set(gold_edge_set)

            intersect_set = test_edge_set.intersection(gold_edge_set)
            correct_num = len(intersect_set)
            gold_set_size = len(gold_edge_set)

            unlabeled_correct_num += correct_num
            unlabeled_gold_set_size += gold_set_size
        data_pool.reset_index()
        return unlabeled_correct_num, unlabeled_gold_set_size

    def __print_result(w_vector, data_pool):
        logger.info("Feature count: %d" % len(w_vector.keys()))
        logger.info("Unlabeled accuracy: %.12f (%d, %d)" % (
            self.unlabeled_correct_num / self.unlabeled_gold_set_size,
            self.unlabeled_correct_num,
            self.unlabeled_gold_set_size))

        """  calculate unlabled attachment accuracy of glm-parser
        unlabeled attachment accuracy = # of corrected tokens in result / # of all corrected tokens
        # of corrected tokens in result = # of corrected edges in result + # of sentences in data set
        # of all corrected tokens = # of all corrected edges + # of sentences in data set
        """
        self.unlabeled_correct_num += data_pool.get_sent_num()
        self.unlabeled_gold_set_size += data_pool.get_sent_num()

        logger.info("Unlabeled attachment accuracy: %.12f (%d, %d)" % (
            self.unlabeled_correct_num / self.unlabeled_gold_set_size,
            self.unlabeled_correct_num,
            self.unlabeled_gold_set_size))
        return

    def sequentialEvaluate(self,
                           data_pool,
                           parser,
                           w_vector,
                           tagger=None,
                           sparkContext=None,
                           hadoop=None):

        self.unlabeled_correct_num = 0
        self.unlabeled_gold_set_size = 0

        logger.debug("Start evaluating ...")
        wv = {}
        for key in w_vector.keys():
            wv[key] = w_vector[key]

        self.unlabeled_correct_num, self.unlabeled_gold_set_size =\
            __evaluate_on_datapool(data_pool=data_pool,
                                   weight_vector=wv,
                                   parser=parser,
                                   tagger=tagger,
                                   hadoop=hadoop)

        self.__print_result(w_vector, data_pool)

    def parallelEvaluate(self,
                         data_pool,
                         parser,
                         w_vector,
                         tagger=None,
                         sparkContext=None,
                         hadoop=None):

        def create_dp(textString, fgen, format, comment_sign):
            dp = data_pool.DataPool(textString   = textString[1],
                                    fgen         = fgen,
                                    format_list  = format,
                                    comment_sign = comment_sign)
            return dp

        self.unlabeled_correct_num = 0
        self.unlabeled_gold_set_size = 0

        logger.debug("Start evaluating ...")

        dir_name     = dataPool.loadedPath()
        format_list  = dataPool.format_list
        comment_sign = dataPool.comment_sign
        fgen         = dataPool.fgen

        sc = sparkContext

        if hadoop is True:
            test_files = sc.wholeTextFiles(dir_name, minPartitions=10).cache()
        else:
            dir_name = os.path.abspath(os.path.expanduser(dir_name))
            test_files = sc.wholeTextFiles("file://" + dir_name, minPartitions=10).cache()

        dp = test_files.map(lambda t: data_pool.DataPool(textString   = t[1],
                                                         fgen         = fgen,
                                                         format       = format_list,
                                                         comment_sign = comment_sign)).cache()
        wv = {}
        for key in w_vector.keys():
            wv[key] = w_vector[key]

        total_sent = dp.map(lambda dp: dp.get_sent_num()).sum()
        logger.info("Totel number of sentences: %d" % total_sent)
        dp = dp.flatMap(lambda t: __evaluate_on_datapool(data_pool     = t,
                                                         weight_vector = wv,
                                                         parser        = parser,
                                                         tagger        = tagger))

        self.unlabeled_correct_num, self.unlabeled_gold_set_size = \
            dp.reduce(lambda a, b: (a[0] + b[0], a[1] + b[1])).collect()

        self.__print_result(w_vector, data_pool)
