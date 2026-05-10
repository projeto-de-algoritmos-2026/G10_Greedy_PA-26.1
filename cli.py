from models import (
    Sala, Professor, Aula,
    Alocacao, AulaRejeitada, ResultadoAlocacao,
)

# helpers de formatação

SLOT_LABELS = [
    "08:00", "09:00", "10:00", "11:00",
    "12:00", "13:00", "14:00", "15:00",
    "16:00", "17:00", "18:00", "19:00",
    "20:00", "21:00",
]

def slot_para_hora(slot: int) -> str:
    if 0 <= slot < len(SLOT_LABELS):
        return SLOT_LABELS[slot]
    return f"slot{slot}"

def intervalo(aula: Aula) -> str:
    return f"{slot_para_hora(aula.slot_inicio)}-{slot_para_hora(aula.slot_fim)}"

def separador(char: str = "─", largura: int = 56) -> None:
    print(char * largura)

def cabecalho(titulo: str) -> None:
    separador("═")
    print(f"  {titulo}")
    separador("═")

def _id_unico(ids_existentes: set[str], prefixo: str) -> str:
    """Sugere o próximo ID sequencial que ainda não existe."""
    i = 1
    while f"{prefixo}{i}" in ids_existentes:
        i += 1
    return f"{prefixo}{i}"


# cadastrar de sala

def cadastrar_sala(salas: list[Sala]) -> Sala | None:
    cabecalho("Cadastrar Sala")
    ids_existentes = {s.id for s in salas}

    sugestao = _id_unico(ids_existentes, "S")
    raw_id = input(f"  ID da sala [{sugestao}]: ").strip()
    sala_id = raw_id if raw_id else sugestao

    if sala_id in ids_existentes:
        print(f"  [ERRO] Já existe uma sala com ID '{sala_id}'.")
        return None

    while True:
        raw = input("  Capacidade (número de alunos): ").strip()
        if raw.isdigit() and int(raw) > 0:
            capacidade = int(raw)
            break
        print("  [ERRO] Informe um número inteiro maior que zero.")

    sala = Sala(id=sala_id, capacidade=capacidade)
    print(f"  [OK] Sala '{sala_id}' com capacidade {capacidade} cadastrada.")
    return sala


# ── cadastro de professor ─────────────────────────────────────────────────────

def cadastrar_professor(professores: list[Professor]) -> Professor | None:
    cabecalho("Cadastrar Professor")
    ids_existentes = {p.id for p in professores}

    sugestao = _id_unico(ids_existentes, "P")
    raw_id = input(f"  ID do professor [{sugestao}]: ").strip()
    prof_id = raw_id if raw_id else sugestao

    if prof_id in ids_existentes:
        print(f"  [ERRO] Já existe um professor com ID '{prof_id}'.")
        return None

    nome = input("  Nome completo: ").strip()
    if not nome:
        print("  [ERRO] Nome não pode ser vazio.")
        return None

    print("  Informe as matérias que o professor pode lecionar, separadas por vírgula.")
    print("  Exemplo: Matemática, Física, Química")
    raw_materias = input("  > ").strip()
    materias = {m.strip() for m in raw_materias.split(",") if m.strip()}
    if not materias:
        print("  [ERRO] Informe ao menos uma matéria.")
        return None

    prof = Professor(id=prof_id, nome=nome, materias=materias)
    mat_str = ", ".join(sorted(prof.materias))
    print(f"  [OK] Prof. '{nome}' ({prof_id}) — matérias: {mat_str}")
    return prof


# cadastrar aula 

def _ler_slot(mensagem: str, min_slot: int = 0, max_slot: int = 13) -> int:
    while True:
        print("  Informe o número do slot desejado.")
        print(f"  Slots válidos: {min_slot} = {slot_para_hora(min_slot)} … {max_slot} = {slot_para_hora(max_slot)}")
        if "exclusivo" in mensagem.lower():
            print("  Observação: o horário final não pode ser igual ao horário de início e é exclusivo — a aula termina antes deste slot.")
        raw = input(f"  {mensagem}: ").strip()
        if raw.isdigit():
            v = int(raw)
            if min_slot <= v <= max_slot:
                return v
        print(f"  [ERRO] Informe um número entre {min_slot} e {max_slot}.")

def cadastrar_aula(aulas: list[Aula], materias_disponiveis: set[str]) -> Aula | None:
    cabecalho("Cadastrar Aula")
    ids_existentes = {a.id for a in aulas}

    sugestao = _id_unico(ids_existentes, "A")
    raw_id = input(f"  ID da aula [{sugestao}]: ").strip()
    aula_id = raw_id if raw_id else sugestao

    if aula_id in ids_existentes:
        print(f"  [ERRO] Já existe uma aula com ID '{aula_id}'.")
        return None

    if materias_disponiveis:
        print("  Matérias já cobertas por professores: " + ", ".join(sorted(materias_disponiveis)))
    print("  Informe a matéria da aula. O valor deve corresponder a uma disciplina.")
    materia = input("  Matéria: ").strip()
    if not materia:
        print("  [ERRO] Matéria não pode ser vazia.")
        return None

    max_inicio = len(SLOT_LABELS) - 2
    slot_inicio = _ler_slot("Slot de início", max_slot=max_inicio)
    slot_fim = _ler_slot(
        "Slot de fim (exclusivo)",
        min_slot=slot_inicio + 1,
        max_slot=len(SLOT_LABELS) - 1,
    )

    while True:
        raw = input("  Quantidade de alunos: ").strip()
        if raw.isdigit() and int(raw) > 0:
            qtd_alunos = int(raw)
            break
        print("  [ERRO] Informe um número inteiro maior que zero.")

    aula = Aula(
        id=aula_id,
        materia=materia,
        slot_inicio=slot_inicio,
        slot_fim=slot_fim,
        qtd_alunos=qtd_alunos,
    )
    print(f"  [OK] Aula '{aula_id}' ({materia}, {intervalo(aula)}, {qtd_alunos} alunos) cadastrada.")
    return aula


# listar cadastros

def listar_cadastros(
    salas: list[Sala],
    professores: list[Professor],
    aulas: list[Aula],
) -> None:
    cabecalho("Cadastros Atuais")

    # salas
    print(f"\n  SALAS ({len(salas)})")
    if salas:
        print(f"  {'ID':<8} {'Capacidade':>10}")
        separador()
        for s in sorted(salas, key=lambda x: x.id):
            print(f"  {s.id:<8} {s.capacidade:>10}")
    else:
        print("  (nenhuma sala cadastrada)")

    # professores
    print(f"\n  PROFESSORES ({len(professores)})")
    if professores:
        print(f"  {'ID':<8} {'Nome':<20} {'Matérias'}")
        separador()
        for p in sorted(professores, key=lambda x: x.id):
            mat_str = ", ".join(sorted(p.materias))
            print(f"  {p.id:<8} {p.nome:<20} {mat_str}")
    else:
        print("  (nenhum professor cadastrado)")

    # aulas
    print(f"\n  AULAS ({len(aulas)})")
    if aulas:
        print(f"  {'ID':<8} {'Matéria':<18} {'Horário':<14} {'Alunos':>6}")
        separador()
        for a in sorted(aulas, key=lambda x: (x.slot_inicio, x.id)):
            print(f"  {a.id:<8} {a.materia:<18} {intervalo(a):<14} {a.qtd_alunos:>6}")
    else:
        print("  (nenhuma aula cadastrada)")

    print()


# exibir resultado da alocação

def exibir_resultado(resultado: ResultadoAlocacao) -> None:
    cabecalho("Resultado da Alocação")

    total = resultado.total_aulas
    alocadas = len(resultado.alocadas)
    taxa = resultado.taxa_alocacao * 100

    print(f"\n  Aulas alocadas : {alocadas} / {total}  ({taxa:.0f}%)")
    separador()

    if resultado.alocadas:
        print("\n  ALOCADAS")
        for aloc in sorted(resultado.alocadas, key=lambda x: x.aula.slot_inicio):
            a = aloc.aula
            print(
                f"\n  [OK]  {a.id} ({a.materia}, {intervalo(a)}, {a.qtd_alunos} alunos)"
            )
            print(
                f"        → Sala {aloc.sala.id} (cap. {aloc.sala.capacidade})"
                f"  |  Prof. {aloc.professor.nome}"
            )

    if resultado.rejeitadas:
        print("\n  NÃO ALOCADAS")
        _motivos = {
            "sem_sala": "sem sala com capacidade disponível no horário",
            "sem_professor": "sem professor disponível para a matéria no horário",
            "ambos": "sem sala E sem professor disponíveis",
        }
        for rej in sorted(resultado.rejeitadas, key=lambda x: x.aula.slot_inicio):
            a = rej.aula
            motivo_desc = _motivos.get(rej.motivo, rej.motivo)
            print(f"\n  [FAIL] {a.id} ({a.materia}, {intervalo(a)}, {a.qtd_alunos} alunos)")
            print(f"         Motivo: {motivo_desc}")

    print()


# menu de persistência (salvar/carregar cenário)

def menu_persistencia(
    salas: list[Sala],
    professores: list[Professor],
    aulas: list[Aula],
) -> tuple[list[Sala], list[Professor], list[Aula]]:
    """Submenu salvar/carregar. Retorna (salas, professores, aulas) — possivelmente alteradas."""
    import persistence  # importação local para não criar dependência circular

    cabecalho("Salvar / Carregar Cenário")
    print("  1. Salvar cenário atual em arquivo")
    print("  2. Carregar cenário de arquivo")
    print("  0. Voltar")
    separador()

    opcao = input("  Opção: ").strip()

    if opcao == "1":
        caminho = input("  Caminho do arquivo (ex: data/cenario.json): ").strip()
        if not caminho:
            print("  [AVISO] Caminho vazio, operação cancelada.")
            return salas, professores, aulas
        try:
            persistence.salvar_cenario(salas, professores, aulas, caminho)
            print(f"  [OK] Cenário salvo em '{caminho}'.")
        except Exception as e:
            print(f"  [ERRO] Não foi possível salvar: {e}")

    elif opcao == "2":
        caminho = input("  Caminho do arquivo (ex: data/cenario.json): ").strip()
        if not caminho:
            print("  [AVISO] Caminho vazio, operação cancelada.")
            return salas, professores, aulas
        try:
            salas, professores, aulas = persistence.carregar_cenario(caminho)
            print(
                f"  [OK] Carregado: {len(salas)} sala(s), "
                f"{len(professores)} professor(es), {len(aulas)} aula(s)."
            )
        except FileNotFoundError:
            print(f"  [ERRO] Arquivo '{caminho}' não encontrado.")
        except Exception as e:
            print(f"  [ERRO] Não foi possível carregar: {e}")

    else:
        if opcao != "0":
            print("  [AVISO] Opção inválida.")

    return salas, professores, aulas