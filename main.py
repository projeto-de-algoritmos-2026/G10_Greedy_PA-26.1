"""
Alocador Guloso de Aulas — entry point
"""
from models import Sala, Professor, Aula, ResultadoAlocacao
import cli

def main() -> None:
    # estado em memória
    salas:      list[Sala]      = []
    professores: list[Professor] = []
    aulas:      list[Aula]      = []
    ultimo_resultado: ResultadoAlocacao | None = None

    while True:
        cli.separador("═")
        print("  Alocador Guloso de Aulas")
        cli.separador("═")
        print("  Digite o número da opção e pressione Enter.")
        print("  1. Cadastrar sala")
        print("  2. Cadastrar professor")
        print("  3. Cadastrar aula")
        print("  4. Listar cadastros")
        print("  5. Executar alocação")
        print("  6. Ver resultado da última alocação")
        print("  7. Salvar / carregar cenário")
        print("  0. Sair")
        cli.separador()
        opcao = input("  Opção: ").strip()

        if opcao == "1":
            sala = cli.cadastrar_sala(salas)
            if sala:
                salas.append(sala)

        elif opcao == "2":
            prof = cli.cadastrar_professor(professores)
            if prof:
                professores.append(prof)

        elif opcao == "3":
            # passa o conjunto de matérias já cobertas para sugerir ao usuário
            materias_cobertas = {m for p in professores for m in p.materias}
            aula = cli.cadastrar_aula(aulas, materias_cobertas)
            if aula:
                aulas.append(aula)

        elif opcao == "4":
            cli.listar_cadastros(salas, professores, aulas)

        elif opcao == "5":
            if not salas:
                print("  [AVISO] Cadastre ao menos uma sala antes de alocar.")
            elif not professores:
                print("  [AVISO] Cadastre ao menos um professor antes de alocar.")
            elif not aulas:
                print("  [AVISO] Cadastre ao menos uma aula antes de alocar.")
            else:
                try:
                    import scheduler
                    ultimo_resultado = scheduler.alocar(salas, professores, aulas)
                    cli.exibir_resultado(ultimo_resultado)
                except ImportError:
                    print("  [ERRO] scheduler.py ainda não foi implementado.")
                except Exception as e:
                    print(f"  [ERRO] Falha ao executar alocação: {e}")

        elif opcao == "6":
            if ultimo_resultado is None:
                print("  [AVISO] Nenhuma alocação executada ainda. Use a opção 5 primeiro.")
            else:
                cli.exibir_resultado(ultimo_resultado)

        elif opcao == "7":
            salas, professores, aulas = cli.menu_persistencia(salas, professores, aulas)
            # limpa resultado anterior se o cenário foi trocado
            ultimo_resultado = None

        elif opcao == "0":
            print("  Até logo!")
            break

        else:
            print("  [AVISO] Opção inválida. Tente novamente.")

        input("\n  Pressione Enter para continuar...")

if __name__ == "__main__":
    main()