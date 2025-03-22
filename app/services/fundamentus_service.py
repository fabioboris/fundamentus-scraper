"""Serviço para coordenar operações com dados do Fundamentus."""

from typing import Any, Dict, Optional

from ..core.extractor import FundamentusExtractor
from ..core.loader import FundamentusLoader
from ..core.transformer import FundamentusTransformer


class FundamentusService:
    """Serviço que coordena as operações de ETL para dados do Fundamentus."""

    def __init__(self, file_path: Optional[str] = None):
        """
        Inicializa o serviço.

        Args:
            file_path: Caminho opcional para salvar os dados
        """
        self.extractor = FundamentusExtractor()
        self.transformer = FundamentusTransformer()
        self.loader = FundamentusLoader()
        self._file_path = file_path

    def etl(self) -> str:
        """
        Executa o processo completo de ETL.

        Returns:
            Caminho do arquivo onde os dados foram salvos
        """
        # Extração
        acoes_raw = self.extractor.extract_acoes()
        fiis_raw = self.extractor.extract_fiis()

        # Transformação
        acoes = self.transformer.transform_acoes(acoes_raw)
        fiis = self.transformer.transform_fiis(fiis_raw)

        # Carregamento
        file_path = self.loader.load(acoes, fiis, self._file_path)
        return file_path

    def get_ticker_indicators(self, ticker: str) -> Dict[str, Any]:
        """
        Obtém e processa os indicadores de um ticker específico.

        Args:
            ticker: Código do ticker a ser consultado

        Returns:
            Dicionário com os indicadores processados
        """
        ticker = ticker.upper()
        raw_data = self.extractor.get_ticker_details(ticker)
        return self.transformer.process_ticker_indicators(raw_data, ticker)

    @property
    def file_path(self) -> str:
        """Retorna o caminho do arquivo onde os dados serão salvos."""
        return self._file_path
