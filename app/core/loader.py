"""Módulo para carregamento de dados processados."""

import os
from typing import Optional

import pandas as pd


class FundamentusLoader:
    """Classe responsável pelo carregamento dos dados processados."""

    def __init__(self, default_path: str = "downloads/fundamentus.xlsx"):
        """
        Inicializa o loader com um caminho padrão.

        Args:
            default_path: Caminho padrão para salvar os dados
        """
        self._default_file_path = default_path

    def load(
        self, acoes: pd.DataFrame, fiis: pd.DataFrame, file_path: Optional[str] = None
    ) -> str:
        """
        Carrega os dados em um arquivo Excel.

        Args:
            acoes: DataFrame com dados de ações
            fiis: DataFrame com dados de FIIs
            file_path: Caminho do arquivo para salvar os dados

        Returns:
            Caminho do arquivo onde os dados foram salvos
        """
        file_path = file_path or self._default_file_path

        # Garantir que o diretório existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with pd.ExcelWriter(file_path) as writer:
            acoes.to_excel(writer, sheet_name="Ações", index=False)
            fiis.to_excel(writer, sheet_name="FIIs", index=False)

        return file_path
