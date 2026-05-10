import json
from pathlib import Path

from models import Aula, Professor, Sala


def salvar_cenario(
    salas: list[Sala],
    professores: list[Professor],
    aulas: list[Aula],
    caminho: str,
) -> None:
    data = {
        "salas": [{"id": s.id, "capacidade": s.capacidade} for s in salas],
        "professores": [
            {"id": p.id, "nome": p.nome, "materias": sorted(p.materias)}
            for p in professores
        ],
        "aulas": [
            {
                "id": a.id,
                "materia": a.materia,
                "slot_inicio": a.slot_inicio,
                "slot_fim": a.slot_fim,
                "qtd_alunos": a.qtd_alunos,
            }
            for a in aulas
        ],
    }
    Path(caminho).write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def carregar_cenario(
    caminho: str,
) -> tuple[list[Sala], list[Professor], list[Aula]]:
    data = json.loads(Path(caminho).read_text(encoding="utf-8"))
    salas = [Sala(id=s["id"], capacidade=s["capacidade"]) for s in data["salas"]]
    professores = [
        Professor(id=p["id"], nome=p["nome"], materias=set(p["materias"]))
        for p in data["professores"]
    ]
    aulas = [
        Aula(
            id=a["id"],
            materia=a["materia"],
            slot_inicio=a["slot_inicio"],
            slot_fim=a["slot_fim"],
            qtd_alunos=a["qtd_alunos"],
        )
        for a in data["aulas"]
    ]
    return salas, professores, aulas
