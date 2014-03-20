SET VS90COMNTOOLS=%VS100COMNTOOLS%
python setup.py build_ext --inplace
python test_glm_parser.py -b 15 -e 15 -o sec_15_15
