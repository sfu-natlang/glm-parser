SET VS90COMNTOOLS=%VS100COMNTOOLS%
python setup.py build_ext --inplace
python test_glm_parser.py -b 2 -e 3 -o sec_02 