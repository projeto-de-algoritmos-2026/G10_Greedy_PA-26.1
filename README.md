# G10_Greedy_PA-26.1

Número da Lista: 2<br>
Conteúdo da Disciplina: Algoritmos Ambiociosos<br>

---

## Alunos
|Matrícula | Aluno |
| :-------: | :------------------------------: |
| 23/1038072  |  Gabriel Dantas Bevilaqua Mendes |
| 23/1026483  |  Maria Eduarda de Amorim Galdino |

---

## Sobre 

Sistema de alocação automática de aulas para escolas, desenvolvido como projeto acadêmico na disciplina de Algoritmos e Estruturas de Dados — UnB.
Dado um conjunto de salas, professores e aulas desejadas, o sistema maximiza o número de aulas alocadas respeitando restrições de capacidade, disponibilidade de sala e disponibilidade de professor.

### Algoritimo

O núcleo do sistema é um algoritmo guloso inspirado no problema clássico de Activity Selection:

As aulas são ordenadas pelo horário de término (critério guloso — libera recursos o quanto antes).
Para cada aula, o sistema busca a menor sala que comporta o número de alunos (evita desperdiçar salas grandes).
Entre os professores disponíveis, escolhe o que já tem mais aulas alocadas (consolida em menos professores).
Se não for possível alocar (sem sala, sem professor ou ambos), a aula é registrada como rejeitada com o motivo.

A abordagem é heurística — pode não encontrar a solução globalmente ótima em todos os casos, mas é eficiente e funciona bem na prática para horários escolares típicos.


---

## Screenshots

---

## Instalação 

**Requisitos:** Python 3.10 ou superior. Nenhuma biblioteca externa necessária.
 
```bash
# Clone o repositório
git clone https://github.com/projeto-de-algoritmos-2026/G10_Greedy_PA-26.1.git

# Acesse o repositório
cd G10_Greedy_PA-26.1
 
# Execute o programa
python3 main.py
```

---

## Link do vídeo
Para acessar a apresentação, clique no link abaixo:

[Assistir ao vídeo](https://youtu.be/link)
