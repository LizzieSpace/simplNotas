import os
import re
from simplNotas import SimplifiedGrades

testfiles = {}
for entry in os.scandir("tests/turmas_teste"):
	rip = re.match(r"(faltas|notas)(\d)", entry.name)
	testfiles[rip[2]] = testfiles.get(rip[2], {})
	testfiles[rip[2]][rip[1]] = entry.path

for files in testfiles.values():
	class_grades = SimplifiedGrades(files["notas"], files["faltas"])
	class_grades.get_avg_grade({"P1": 1, "P2": 2, "P3": 2, "P4": 3, "P5": 3})
	class_grades.get_attendances()
	class_grades.get_performance(class_grades.grades["avg"], push_grades=True)
	print(files)
	print(class_grades.grades.sort_values(by=["avg"], ascending=False), end='\n\n\n\n\n')
