"""Módulo para extração de dados do site Fundamentus."""

from io import StringIO
from typing import Any, Dict

import pandas as pd
import requests
from bs4 import BeautifulSoup


class FundamentusExtractor:
    """Classe responsável pela extração de dados do site Fundamentus."""

    def __init__(self):
        self._user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/112.0.0.0 Safari/537.36"
        )
        self._base_url = "https://www.fundamentus.com.br"
        self._url_acoes = f"{self._base_url}/resultado.php"
        self._url_fiis = f"{self._base_url}/fii_resultado.php"
        self._url_detalhes = f"{self._base_url}/detalhes.php"

    def _get_html_content(self, url: str) -> str:
        """
        Obtém o conteúdo HTML de uma URL.

        Args:
            url: URL para obter o conteúdo

        Returns:
            Conteúdo HTML da página
        """
        headers = {"User-Agent": self._user_agent}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Levanta exceção para erros HTTP
        return response.text

    def _extract_table(self, url: str) -> pd.DataFrame:
        """
        Extrai tabela de dados de uma URL.

        Args:
            url: URL contendo a tabela

        Returns:
            DataFrame com os dados da tabela
        """
        html_content = self._get_html_content(url)
        return pd.read_html(StringIO(html_content), thousands=".", decimal=",")[0]

    def extract_acoes(self) -> pd.DataFrame:
        """
        Extrai dados de ações.

        Returns:
            DataFrame com dados de ações
        """
        return self._extract_table(self._url_acoes)

    def extract_fiis(self) -> pd.DataFrame:
        """
        Extrai dados de FIIs.

        Returns:
            DataFrame com dados de FIIs
        """
        return self._extract_table(self._url_fiis)

    def get_ticker_details(self, ticker: str) -> Dict[str, Any]:
        """
        Obtém detalhes de um ticker específico.

        Args:
            ticker: Código do ticker a ser consultado

        Returns:
            Dicionário com os detalhes do ticker
        """
        url = f"{self._url_detalhes}?papel={ticker}"
        headers = {"User-Agent": self._user_agent}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        data = {}
        table_rows = soup.find_all("tr")
        for row in table_rows:
            cols = row.find_all("td")
            if len(cols) == 6:
                keys = [0, 2, 4]
            elif len(cols) == 4:
                keys = [0, 2]
            else:
                continue

            for col in keys:
                key = cols[col].text.strip().replace("?", "")
                value = cols[col + 1].text.strip().replace(".", "").replace(",", ".")
                data[key] = value

        return data
