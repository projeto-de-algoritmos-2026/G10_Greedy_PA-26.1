from models import (
    Alocacao,
    Aula,
    AulaRejeitada,
    Professor,
    ResultadoAlocacao,
    Sala,
)


def _conflito(inicio: int, fim: int, ocupacoes: list[tuple[int, int]]) -> bool:
    for ini_b, fim_b in ocupacoes:
        if inicio < fim_b and ini_b < fim:
            return True
    return False


def alocar(
    salas: list[Sala],
    professores: list[Professor],
    aulas: list[Aula],
) -> ResultadoAlocacao:
    aulas_ordenadas = sorted(aulas, key=lambda a: (a.slot_fim, a.slot_inicio))

    ocupacao_sala: dict[str, list[tuple[int, int]]] = {s.id: [] for s in salas}
    ocupacao_prof: dict[str, list[tuple[int, int]]] = {p.id: [] for p in professores}
    carga_prof: dict[str, int] = {p.id: 0 for p in professores}

    resultado = ResultadoAlocacao()

    for aula in aulas_ordenadas:
        salas_candidatas = [
            s
            for s in salas
            if s.capacidade >= aula.qtd_alunos
            and not _conflito(aula.slot_inicio, aula.slot_fim, ocupacao_sala[s.id])
        ]
        sala_escolhida = min(salas_candidatas, key=lambda s: s.capacidade, default=None)

        profs_candidatos = [
            p
            for p in professores
            if aula.materia in p.materias
            and not _conflito(aula.slot_inicio, aula.slot_fim, ocupacao_prof[p.id])
        ]
        prof_escolhido = max(profs_candidatos, key=lambda p: carga_prof[p.id], default=None)

        if sala_escolhida is not None and prof_escolhido is not None:
            resultado.alocadas.append(Alocacao(aula, sala_escolhida, prof_escolhido))
            ocupacao_sala[sala_escolhida.id].append((aula.slot_inicio, aula.slot_fim))
            ocupacao_prof[prof_escolhido.id].append((aula.slot_inicio, aula.slot_fim))
            carga_prof[prof_escolhido.id] += 1
        else:
            if sala_escolhida is None and prof_escolhido is None:
                motivo = "ambos"
            elif sala_escolhida is None:
                motivo = "sem_sala"
            else:
                motivo = "sem_professor"
            resultado.rejeitadas.append(AulaRejeitada(aula, motivo))

    return resultado
