import logging
from weight.weight_vector import WeightVector
logger = logging.getLogger('EVALUATOR')


class EvaluatorBase:
    def __init__(self):
        self.correct_num = 0
        self.gold_set_size = 0
        return

    def __print_result(self, w_vector, data_pool):
        logger.info("Feature count: %d" % len(w_vector.keys()))
        logger.info("Unlabeled accuracy: %.12f (%d, %d)" % (
            float(self.unlabeled_correct_num) / self.unlabeled_gold_set_size,
            self.unlabeled_correct_num,
            self.unlabeled_gold_set_size))

        """  calculate unlabled attachment accuracy
        unlabeled attachment accuracy =
            # of corrected tokens in result / # of all corrected tokens
        # of corrected tokens in result =
            # of corrected edges in result + # of sentences in data set
        # of all corrected tokens =
            # of all corrected edges + # of sentences in data set
        """
        self.unlabeled_correct_num += data_pool.get_sent_num()
        self.unlabeled_gold_set_size += data_pool.get_sent_num()

        logger.info("Unlabeled attachment accuracy: %.12f (%d, %d)" % (
            float(self.unlabeled_correct_num) / self.unlabeled_gold_set_size,
            self.unlabeled_correct_num,
            self.unlabeled_gold_set_size))
        return

    def __datapool_evaluator(self,
                             data_pool,
                             weight_vector,
                             sentence_evaluator,
                             hadoop=None):

        w_vector = WeightVector()
        for key in weight_vector:
            w_vector[key] = weight_vector[key]

        unlabeled_correct_num = 0
        unlabeled_gold_set_size = 0

        sentence_count = 1
        data_size = data_pool.get_sent_num()

        while data_pool.has_next_data():
            sent = data_pool.get_next_data()

            if not hadoop:
                logger.info("Sentence %d of %d, Length %d" % (
                    sentence_count,
                    data_size,
                    len(sent.get_word_list()) - 1))
            sentence_count += 1

            correct_num, gold_set_size = \
                sentence_evaluator(sent, w_vector)

            unlabeled_correct_num += correct_num
            unlabeled_gold_set_size += gold_set_size
            print correct_num, gold_set_size, unlabeled_correct_num, unlabeled_gold_set_size
        data_pool.reset_index()
        return unlabeled_correct_num, unlabeled_gold_set_size

    def sequentialEvaluate(self,
                           data_pool,
                           w_vector,
                           sentence_evaluator,
                           sparkContext=None,
                           hadoop=None):
        self.correct_num = 0
        self.gold_set_size = 0

        logger.debug("Start evaluating ...")
        wv = {}
        for key in w_vector.keys():
            wv[key] = w_vector[key]

        self.unlabeled_correct_num, self.unlabeled_gold_set_size =\
            self.__datapool_evaluator(data_pool=data_pool,
                                      weight_vector=wv,
                                      sentence_evaluator=sentence_evaluator,
                                      hadoop=hadoop)

        self.__print_result(w_vector, data_pool)
        return

    def parallelEvaluate(self,
                         data_pool,
                         w_vector,
                         sentence_evaluator,
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
        dp = dp.flatMap(lambda t: self.__datapool_evaluator(data_pool          = t,
                                                            weight_vector      = wv,
                                                            sentence_evaluator = sentence_evaluator))

        self.unlabeled_correct_num, self.unlabeled_gold_set_size = \
            dp.reduce(lambda a, b: (a[0] + b[0], a[1] + b[1])).collect()

        self.__print_result(w_vector, data_pool)
