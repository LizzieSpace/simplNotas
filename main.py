import os
import re
import pandas

# requires scipy
import matplotlib.pyplot as plt
from simplNotas import SimplifiedGrades

testfiles = {}
for entry in os.scandir("tests/turmas_teste"):
	rip = re.match(r"(faltas|notas)(\d)", entry.name)
	testfiles[rip[2]] = testfiles.get(rip[2], {})
	testfiles[rip[2]][rip[1]] = entry.path

for name, files in testfiles.items():
	class_grades = SimplifiedGrades(files["notas"], files["faltas"])
	class_grades.get_avg_grade({"P1": 1, "P2": 2, "P3": 2, "P4": 3, "P5": 3})
	class_grades.get_attendances(inplace=True)
	class_grades.get_performance(class_grades.grades["avg"], inplace=True)
	final_table = class_grades.grades.sort_values(by=["avg"], ascending=False)
	print(files, f"\ncorrelation coefficient between avg & att[%] on class {name}:")
	for x in ['kendall', 'spearman', 'pearson']:
		print(
			f"{x}'s {'' if x=='pearson' else'Rank'}: ",
			class_grades.grades["avg"]
			.corr(class_grades.grades["att[%]"], x))
	print(final_table, end="\n\n\n\n\n")
	final_table.plot(
		x="att[%]", y="avg",
		kind='scatter',
		title=f'Turma {name}:',
		xlabel="Frequência [%]",
		ylabel="Nota"
		)

# plt.show()
