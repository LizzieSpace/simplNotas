import pandas as pd
from pdcast import downcast


class simplNotas:
	"""
	:param path_notas: Caminho do arquivo de notas.
	:param path_faltas: [Opcional] Caminho do arquivo de faltas.
	"""

	def __init__(self, path_notas: str, path_faltas: str = ...) -> None:
		self._notas = downcast(pd.read_fwf(path_notas, index_col=0))
		self.notas = pd.DataFrame = self._notas
		self.media: pd.DataFrame = ...
		self._faltas = downcast(
			pd.read_fwf(path_faltas, header=None, index_col=0)
			).infer_objects() if path_faltas is not None else None

	def __rep_faltas(self, nome_aluno: str) -> bool:
		"""
		:return: True se reprovado
		"""
		counts = self._faltas.loc[nome_aluno].value_counts()
		return True if counts[False] / counts.sum() > .25 else False

	def media(self, pesos: dict = ...):# TODO: Testar media e resolver erros
		"""
		Calcula a media ponderada para todos na turma.\n
		{<colname>: <value>,...} para cada coluna na média
		:param pesos: e.g.: {"P1": 1,"P2":2,...}
		:return: pandas.Series com a media ponderada para todos os alunos
		"""
		if pesos is ...:
			pesos = {}
			for Pn in self._notas.columns:
				pesos[Pn] = 1
		try:
			sum_p = pd.Series([0 for nome in self._notas.index])
			for nome, peso in pesos.items():
				sum_p += self._notas[nome] * peso
			self.media = sum_p / sum(pesos.values())
			return self.media
		except KeyError:
			print(KeyError)
			return None

	def rendimento(self): #TODO terminar rendimento

		for nome, nota in self.media.items():
			match nota:
				case _ if 10 >= nota >= 9.0: self.notas["rendimento"][nome] = "SS"
				case _ if 9.0 > nota >= 7.0: self.notas["rendimento"] = "MS"
				case _ if 7.0 > nota >= 5.0: self.notas["rendimento"] = "MM"
				case _ if 5.0 > nota >= 3.0: self.notas["rendimento"] = "MI"
				case _ if 3.0 > nota > 0: self.notas["rendimento"] = "II"
				case _ if nota == 0: self.notas["rendimento"] = "SR"
			if self.__rep_faltas(nome):
				self.notas["rendimento"] = "SR"


su = simplNotas('notas1.txt', 'faltas1.txt')
