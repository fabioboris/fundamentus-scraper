"""Interface de linha de comando para o aplicativo."""

from typing import Any, Dict


class FundamentusCLI:
    """Interface de linha de comando para exibição de dados do Fundamentus."""

    @staticmethod
    def display_ticker_indicators(indicators: Dict[str, Any]) -> None:
        """
        Exibe os indicadores de um ticker específico.

        Args:
            indicators: Dicionário com os indicadores processados
        """
        print("-" * 40)
        print(f"Ticker: {indicators.get('ticker', '')}")
        print(f"Data da última cotação: {indicators.get('dt_cotacao', '')}")
        print(f"Cotação: R$ {indicators.get('cotacao', 0):.2f}")

        if "dy" in indicators:
            print(f"DY: {indicators.get('dy', 0)*100:.2f}%")

        if "pvp" in indicators:
            print(f"P/VP: {indicators.get('pvp', 0):.2f}")

        print("-" * 40)

    @staticmethod
    def display_etl_success(file_path: str) -> None:
        """
        Exibe mensagem de sucesso após ETL.

        Args:
            file_path: Caminho do arquivo onde os dados foram salvos
        """
        print(f"Dados salvos com sucesso em: {file_path}")
