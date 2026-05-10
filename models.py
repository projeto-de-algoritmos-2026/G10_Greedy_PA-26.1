from dataclasses import dataclass, field


@dataclass
class Sala:
    id: str
    capacidade: int


@dataclass
class Professor:
    id: str
    nome: str
    materias: set[str] = field(default_factory=set)


@dataclass
class Aula:
    id: str
    materia: str
    slot_inicio: int
    slot_fim: int
    qtd_alunos: int


@dataclass
class Alocacao:
    aula: Aula
    sala: Sala
    professor: Professor


@dataclass
class AulaRejeitada:
    aula: Aula
    motivo: str


@dataclass
class ResultadoAlocacao:
    alocadas: list[Alocacao] = field(default_factory=list)
    rejeitadas: list[AulaRejeitada] = field(default_factory=list)

    @property
    def total_aulas(self) -> int:
        return len(self.alocadas) + len(self.rejeitadas)

    @property
    def taxa_alocacao(self) -> float:
        total = self.total_aulas
        return len(self.alocadas) / total if total else 0.0
