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
		self._faltas = downcast(
			pd.read_fwf(path_faltas, header=None, index_col=0)
			).infer_objects() if path_faltas is not None else None

	def __rep_faltas(self, nome_aluno: str) -> bool:
		"""
		:return: True se reprovado
		"""
		reprovado = False
		counts = self._faltas.loc[nome_aluno].value_counts()
		match counts.size:
			case 1: reprovado = not counts.index[0]
			case 2: reprovado = False if counts[True] / counts.sum() > .75 else True
			case _: raise KeyError("Os valores na tabela de faltas está correta? ")
		return reprovado

	def get_media(self, pesos: dict = ...):
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
			sum_p = pd.Series([0 for i in self._notas.index], index=self._notas.index, name="media")
			for nome, peso in pesos.items():
				sum_p += self._notas[nome] * peso
			return sum_p / sum(pesos.values())
		except KeyError:
			print(KeyError)
			return None

	def rendimento(self, notas_finais: pd.Series):
		rendimento = pd.Series([], name="rendimento")
		for nome, nota in notas_finais.items():
			match nota:
				case _ if 10 >= nota >= 9.0: rendimento[nome] = "SS"
				case _ if 9.0 > nota >= 7.0: rendimento[nome] = "MS"
				case _ if 7.0 > nota >= 5.0: rendimento[nome] = "MM"
				case _ if 5.0 > nota >= 3.0: rendimento[nome] = "MI"
				case _ if 3.0 > nota > 0: rendimento[nome] = "II"
				case _ if nota == 0: rendimento[nome] = "SR"
			if self.__rep_faltas(nome):
				rendimento[nome] = "SR"
		return rendimento


su = simplNotas('notas1.txt', 'faltas1.txt')
media = su.get_media({"P1": 1, "P2": 2, 'P3': 2, 'P4': 3, 'P5': 3})
print(su.rendimento(media))
