SET VS90COMNTOOLS=%VS100COMNTOOLS%
python setup.py build_ext --inplace
python glm_parser.py -b 14 -e 14 -o sec_14_14
