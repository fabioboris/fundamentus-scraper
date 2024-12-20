from io import StringIO
from typing import Optional

import pandas as pd
import requests


class Fundamentus:
    """Fundamentus ETL class."""

    def __init__(self, file_path: Optional[str] = None):
        self.__default_file_path = "downloads/fundamentus.xlsx"
        self.__file_path = file_path if file_path else f"{self.__default_file_path}"

        self.__user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/112.0.0.0 Safari/537.36"
        )
        self.__base_url = "https://www.fundamentus.com.br"
        self.__url_acoes = f"{self.__base_url}/resultado.php"
        self.__url_fiis = f"{self.__base_url}/fii_resultado.php"

    def __get_html_content(self, url: str) -> str:
        headers = {
            "User-Agent": self.__user_agent,
        }
        response = requests.get(url, headers=headers, timeout=None)
        return response.text

    def __extract_table(self, url: str) -> pd.DataFrame:
        html_content = self.__get_html_content(url)
        return pd.read_html(StringIO(html_content), thousands=".", decimal=",")[0]

    def __extract_acoes(self) -> pd.DataFrame:
        return self.__extract_table(self.__url_acoes)

    def __extract_fiis(self) -> pd.DataFrame:
        return self.__extract_table(self.__url_fiis)

    def __format_as_percent(self, column: pd.Series) -> pd.Series:
        return (
            pd.to_numeric(
                column.str.replace("%", "").str.replace(".", "").str.replace(",", ".")
            )
            / 100
        )

    def __transform_acoes(self, acoes: pd.DataFrame) -> pd.DataFrame:
        for col in [
            "Div.Yield",
            "Mrg Ebit",
            "Mrg. Líq.",
            "ROIC",
            "ROE",
            "Cresc. Rec.5a",
        ]:
            acoes[col] = self.__format_as_percent(acoes[col])

        return acoes

    def __transform_fiis(self, fiis: pd.DataFrame) -> pd.DataFrame:
        for col in ["FFO Yield", "Dividend Yield", "Cap Rate", "Vacância Média"]:
            fiis[col] = self.__format_as_percent(fiis[col])

        return fiis

    def __load(self, acoes: pd.DataFrame, fiis: pd.DataFrame, file_name: str) -> None:
        with pd.ExcelWriter(file_name) as writer:
            acoes.to_excel(writer, sheet_name="Ações", index=False)
            fiis.to_excel(writer, sheet_name="FIIs", index=False)

    def etl(self, file_name: Optional[str] = None) -> None:
        """
        Extract, transform and load data.

        Args:
            file_name: The name of the file to save the data.
                If None, the default file name will be used.
        """
        acoes = self.__extract_acoes()
        acoes = self.__transform_acoes(acoes)

        fiis = self.__extract_fiis()
        fiis = self.__transform_fiis(fiis)

        if file_name is None:
            file_name = self.__file_path

        self.__load(acoes, fiis, file_name)
