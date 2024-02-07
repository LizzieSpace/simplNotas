import pandas as pd
from pdcast import downcast


class SimplifiedGrades:

	def __init__(
		self, grades: pd.DataFrame | str = None,
		absences: pd.DataFrame | str = None
		) -> None:
		"""
		Parameters
		----------
		grades : pd.DataFrame or str, optional
			The grades' data. If provided as a string, it should be the path to a file containing the grades' data.
			If provided as a pd.DataFrame, it should be a dataframe containing the grades' data. (default: None)

		absences : pd.DataFrame or str, optional
			The absences' data. If provided as a string, it should be the path to a file containing the absences' data.
			If provided as a pd.DataFrame, it should be a dataframe containing the absences' data. (default: None)

		Notes
		-----
		Currently, the grades and absences parameters, when strings, assume the file contains a table of fixed-width
		formatted lines.
		"""
		match grades:
			case str(): self._grades = downcast(pd.read_fwf(grades, index_col=0))
			case pd.DataFrame(): self._grades = downcast(grades)
			case _: self.absences = None

		match absences:
			case str(): self._absences = downcast(pd.read_fwf(absences, header=None, index_col=0).infer_objects())
			case pd.DataFrame(): self._absences = absences.astype(bool)
			case _: self._absences = None

		self.grades: pd.DataFrame = \
			self._grades if type(self._grades) is pd.DataFrame else pd.DataFrame(self._grades)

		self.DEFAULT_WEIGHTS = self.__default_weights()

	def __has_many_absences(self, student_name) -> bool:
		counts = self._absences.loc[student_name].value_counts(normalize=True)
		match counts.size:
			case 1: return not counts.index[0]
			case 2: return False if counts[True] > .75 else True
			case _: raise KeyError("The values in the absences table are correct? ")

	def __default_weights(self):
		return {Pn: 1 for Pn in (self._grades.columns if type(self._grades) is pd.DataFrame else range(1))}

	def get_avg_grade(self, weights: dict = None, push_grades: bool = True) -> pd.Series:
		"""
		Parameters
		----------
		weights : dict, optional
			The weights to be used for calculating the average grade. If not provided, default weights will be used.
			The keys of the dictionary should be the names of the grades, and the values should be the corresponding
			weights.
			Default value is None.

		push_grades : bool, optional
			A flag indicating whether to update the 'avg' grade in the `self.grades` DataFrame with the calculated
			average grade.
			Default value is True.

		Returns
		-------
		pd.Series
			If successful, returns a pandas Series object containing the calculated average grade for each student.
			If any of the grade names in `weights` are not found in `self._grades`, throws KeyError.

		Examples
		--------
		Here is an example of how to calculate the average grades for a class:

		>>> class_grades = pd.DataFrame({
		...     'P1': [ 4.5,   6.7,  8.5 ],
		...     'P2': [ 5.6,   7.8,  9.1 ]},
		...     index=['John','Kate','Elijah'])
		>>> test_weights = {'P1': 0.4, 'P2': 0.6}
		>>> classGrades = SimplifiedGrades(class_grades)
		>>> avg_grades = classGrades.get_avg_grade(test_weights)
		>>> avg_grades
		John      5.16
		Kate      7.36
		Elijah    8.86
		Name: avg, dtype: float64

		In this example, we have a DataFrame called `class_grades` with grades for 3 students John, Kate and Elijah
		for two different tests 'P1' and 'P2'. We initialize a `SimplifiedGrades` object with this DataFrame.

		We then calculate the average grade for each student using the `get_avg_grade` method of the
		`SimplifiedGrades` class passing the test_weights dictionary. This will return a pandas Series with the
		average grade for each student.
		"""

		if weights is None:
			weights = self.__default_weights()
		try:
			weighted_sum = pd.Series([0 for _ in self._grades.index], index=self._grades.index)
			for name, weight in weights.items():
				weighted_sum = weighted_sum.add(self._grades[name].mul(weight))
			avg = weighted_sum.div(sum(weights.values())).round(2)
			avg.name = 'avg'
			if push_grades:
				self.grades["avg"] = avg
			return avg
		except KeyError:
			print(KeyError)

	@staticmethod
	def _calculate_grade(grade):
		"""
		Parameters
		----------
		grade : float
			The grade value to calculate the performance of.

		Returns
		-------
		str
			The calculated performance based on the grade value.

			* "ERR" if the grade parameter does not fit within the interval of [0,10]
		"""
		performance: str = "ERR"
		match grade:
			case _ if 10 >= grade >= 9.0: performance = "SS"
			case _ if 9.0 > grade >= 7.0: performance = "MS"
			case _ if 7.0 > grade >= 5.0: performance = "MM"
			case _ if 5.0 > grade >= 3.0: performance = "MI"
			case _ if 3.0 > grade > 0: performance = "II"
			case _ if grade == 0: performance = "SR"

		return performance

	def get_performance(self, final_grades: pd.Series, push_grades: bool = False) -> pd.Series:
		"""
		This method takes the final grades of students and assigns performance grades.

		Parameters
		----------
		final_grades : pandas.Series
			A Series containing the final grades of students.
		push_grades : bool, optional
			A boolean indicating whether to push the performance grades to the 'perf' column in the
			grades DataFrame, by default False

		Returns
		-------
		pandas.Series
			A pandas Series containing the performance grades of each student. The returned performance grades are
			of type 'category' in order to optimize memory usage.

		Notes
		-----
		The performance grade is assigned based on the following scale: \n
		- If the grade is between 10.0 and 9.0 (inclusive), the performance grade is "SS".
		- If the grade is between 9.0 and 7.0 (inclusive), the performance grade is "MS".
		- If the grade is between 7.0 and 5.0 (inclusive), the performance grade is "MM".
		- If the grade is between 5.0 and 3.0 (inclusive), the performance grade is "MI".
		- If the grade is between 3.0 and 0.0 (exclusive), the performance grade is "II".
		- If the grade is 0.0, the performance grade is "SR".
		If a student has many absences, their performance grade is automatically set to "SR".
		If push_grades is True, the performance grades will be pushed to the 'perf' column in the grades DataFrame.

		Examples
		--------
		>>> class_grades = pd.DataFrame({
		...     'P1': [ 4.5,   1.2,   6.7 ],
		...     'P2': [ 9.1,   7.8,   8.9 ]},
		...     index=['John','Kate','Elijah'])
		>>> classGrades = SimplifiedGrades(class_grades)
		>>> avg_grades = classGrades.get_avg_grade()
		>>> classGrades.get_performance(avg_grades)
		John      MM
		Kate      MI
		Elijah    MS
		Name: performance, dtype: category
		Categories (3, object): ['MI', 'MM', 'MS']
		"""
		performance = pd.Series([], name="performance")
		for name, grade in final_grades.items():
			performance[name] = self._calculate_grade(grade)

			if self._absences:
				if self.__has_many_absences(name):
					performance[name] = "SR"

		if push_grades:
			self.grades["perf"] = performance.astype("category")
		return performance.astype("category")

# grades = pd.DataFrame({'P1': [8.5, 7.2, 6.7], 'P2': [9.1, 7.8, 8.9]}, index=['John', 'Kate', 'Elijah'])
# absences = pd.DataFrame({'John': [False, True, False], 'Kate': [False, False, True], 'Elijah': [False, False,
# False]}).T
# classGrades = SimplifiedGrades(grades, absences)
# avg_grade = classGrades.get_avg_grade()
# performance = classGrades.get_performance(avg_grade)
