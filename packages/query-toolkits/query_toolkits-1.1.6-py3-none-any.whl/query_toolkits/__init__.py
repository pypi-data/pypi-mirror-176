# import os,sys
# os.chdir(sys.path[0])
from query_toolkits.extractor import Extractor
from query_toolkits.error_correction import Corrector

et = Extractor()
extract_time = et.extract_time
extract_number = et.extract_number
extract_requirement = et.extract_requirement
extract_reference_no = et.extract_reference_no

c = Corrector()
correct = c.correct
