import pandas as pd


class simplNotas:
	def __init__(self, path_notas: str, path_faltas: str = None):
		self._notas = pd.read_fwf(path_notas).convert_dtypes()
		self._faltas = pd.read_fwf(path_faltas, header=None).convert_dtypes()  # TODO transformar int -> bool
