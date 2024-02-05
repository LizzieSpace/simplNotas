### Objetivos do projeto:

- [ ] Calcular a média ponderada de todos os alunos
  - [ ] atribuir as menções
  - [ ] reorganizar a lista em ordem de *notas* [^1] (não de menção).

- [ ] Ler a lista de presença [1 significa presente, 0 falta]
  - [ ] Reprovar automaticamente com SR alunos com 25% (ou mais) de faltas, não importando sua menção.

- [ ] Fazer a melhor análise que puder, para tentar mostrar se nesta turma em específico existe relação aparente entre a nota do aluno e o número de faltas.

> <sub> O código deve funcionar para qualquer .txt que possua o mesmo formato (podendo alterar o numero de alunos e os seus nomes). </sub>
---
> [!IMPORTANT]
> Durante o desenvolvimento, use a branch `dev`. Uma vez que o código para essa 'feature' estiver pronto e estável, crie um pull request para a branch `prod`

[^1]: *A primeira prova possui peso 1, a segunda e a terceira possuem peso 2, a quarta e a quinta possuem peso 3.*