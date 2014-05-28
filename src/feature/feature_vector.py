from hvector._mycollections import mydefaultdict
from hvector.mydouble import mydouble

class FeatureVector():
    """
    Emulates a feature vector using dictionary indtead of list
    """
    def __init__(self):
        #self.feature_dict = {}
        # changed to hvector
        self.feature_dict = mydefaultdict(mydouble)
        return

    def __getitem__(self,feature_str):
        return self.feature_dict[feature_str]

    def __setitem__(self,feature_str,feature_count):
        self.feature_dict[feature_str] = feature_count

    def has_key(self,feature_str):
        return self.feature_dict.has_key(feature_str)

    def keys(self):
        return self.feature_dict.keys()
    def aggregate(self,another_fv):
        """
        Aggregate another feature vector into this one, no return value

        :param another_fv: The feature vector that you want to aggregate
        :type another_fv: FeatureVector
        """
        # change to hvector
        #for i in another_fv.keys():
        #    # If the feature also exists in this vector then add them up
        #    if self.has_key(i):
        #        self[i] += another_fv[i]
        #    # If it does not exist just copy the value
        #    else:
        #        self[i] = another_fv[i]
        self.feature_dict.iadd(another_fv.feature_dict)
        return

    def eliminate(self,another_fv):
        """
        Eliminate another feature vector from this one, no return value

        :param another_fv: The feature vector that you want to eliminate
        :type another_fv: FeatureVector
        """
        # change to hvector
        # for i in another_fv.keys():
        #    # If the feature also exists in this vector then add them up
        #    if self.has_key(i):
        #        self[i] -= another_fv[i]
        #    # If it does not exist just copy the value
        #    else:
        #        self[i] = -another_fv[i]
        self.feature_dict.iaddc(another_fv.feature_dict, -1)
        return
    
    def __add__(self,another_fv):
        """
        Arrgegate two feature vectors into one, and return a new feature vector
        
        :param another_fv: The feature vector that you want to aggregate
        :type another_fv: FeatureVector
        """
        ret_vector = FeatureVector()
        # These two aggregations make it slow. So do not use this overload
        # unless necessary
        ret_vector.aggregate(self)
        ret_vector.aggregate(another_fv)
        return ret_vector

    def __sub__(self,another_fv):
        ret_vector = FeatureVector()
        ret_vector.aggregate(self)
        ret_vector.eliminate(another_fv)
        return ret_vector
