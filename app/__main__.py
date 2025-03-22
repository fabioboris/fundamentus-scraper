"""Ponto de entrada principal do aplicativo."""

import argparse
import sys

from .services.fundamentus_service import FundamentusService
from .ui.cli import FundamentusCLI


def main():
    """Função principal do programa."""
    parser = argparse.ArgumentParser(
        description="Ferramenta para obter fundamentos de ações e FIIs"
    )

    # Cria um grupo mutuamente exclusivo para os argumentos -t e -o
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-o",
        "--output",
        help="Caminho para salvar o arquivo Excel com os dados",
        default=None,
    )

    group.add_argument(
        "-t",
        "--ticker",
        help="Ticker do ativo para exibir indicadores específicos",
        default=None,
    )

    args = parser.parse_args()

    try:
        service = FundamentusService(file_path=args.output)
        cli = FundamentusCLI()

        if args.ticker:
            indicators = service.get_ticker_indicators(args.ticker)
            cli.display_ticker_indicators(indicators)
        else:
            file_path = service.etl()
            cli.display_etl_success(file_path)

    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
