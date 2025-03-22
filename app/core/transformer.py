"""Módulo para transformação de dados extraídos do Fundamentus."""

from typing import Any, Dict

import pandas as pd


class FundamentusTransformer:
    """Classe responsável pela transformação dos dados extraídos."""

    def _format_as_percent(self, column: pd.Series) -> pd.Series:
        """
        Converte uma coluna de texto com percentual para valor numérico.

        Args:
            column: Série pandas contendo valores percentuais como texto

        Returns:
            Série pandas com valores convertidos para números decimais
        """
        return (
            pd.to_numeric(
                column.str.replace("%", "").str.replace(".", "").str.replace(",", "."),
                errors="coerce",
            )
            / 100
        )

    def transform_acoes(self, acoes: pd.DataFrame) -> pd.DataFrame:
        """
        Transforma dados de ações.

        Args:
            acoes: DataFrame com dados brutos de ações

        Returns:
            DataFrame com dados transformados
        """
        acoes_copy = acoes.copy()

        percent_columns = [
            "Div.Yield",
            "Mrg Ebit",
            "Mrg. Líq.",
            "ROIC",
            "ROE",
            "Cresc. Rec.5a",
        ]

        for col in percent_columns:
            if col in acoes_copy.columns:
                acoes_copy[col] = self._format_as_percent(acoes_copy[col])

        return acoes_copy

    def transform_fiis(self, fiis: pd.DataFrame) -> pd.DataFrame:
        """
        Transforma dados de FIIs.

        Args:
            fiis: DataFrame com dados brutos de FIIs

        Returns:
            DataFrame com dados transformados
        """
        fiis_copy = fiis.copy()

        percent_columns = ["FFO Yield", "Dividend Yield", "Cap Rate", "Vacância Média"]

        for col in percent_columns:
            if col in fiis_copy.columns:
                fiis_copy[col] = self._format_as_percent(fiis_copy[col])

        return fiis_copy

    def process_ticker_indicators(
        self, data: Dict[str, Any], ticker: str
    ) -> Dict[str, Any]:
        """
        Processa os indicadores de um ticker específico.

        Args:
            data: Dicionário com dados brutos do ticker
            ticker: Código do ticker

        Returns:
            Dicionário com indicadores processados
        """
        processed = {"ticker": ticker.upper()}

        # Valores básicos
        processed["dt_cotacao"] = data.get("Data últ cot", "")

        try:
            processed["cotacao"] = float(data.get("Cotação", 0))
        except (ValueError, TypeError):
            processed["cotacao"] = 0.0

        # Determina se é ação ou FII e processa adequadamente
        try:
            # Patrimônio líquido
            if "Patrim Líquido" in data:
                processed["patr_liq"] = float(data.get("Patrim Líquido", 0))
            elif "Patrim. Líq" in data:
                processed["patr_liq"] = float(data.get("Patrim. Líq", 0))
            else:
                processed["patr_liq"] = 0.0

            # Número de cotas/ações
            if "Nro. Cotas" in data:
                processed["nr_cotas"] = float(data.get("Nro. Cotas", 0))
            elif "Nro. Ações" in data:
                processed["nr_cotas"] = float(data.get("Nro. Ações", 0))
            else:
                processed["nr_cotas"] = 0.0

            # Dividend Yield
            if "Div. Yield" in data:
                dy_str = data.get("Div. Yield", "0").strip("%")
                processed["dy"] = float(dy_str) / 100 if dy_str else 0.0
            else:
                processed["dy"] = 0.0

            # Cálculos derivados
            processed["div_cota"] = processed["cotacao"] * processed["dy"]

            if processed["nr_cotas"] != 0:
                processed["patr_cota"] = processed["patr_liq"] / processed["nr_cotas"]
            else:
                processed["patr_cota"] = 0.0

            if processed["patr_cota"] != 0:
                processed["pvp"] = processed["cotacao"] / processed["patr_cota"]
            else:
                processed["pvp"] = 0.0

        except (ValueError, TypeError) as e:
            # Log do erro e continua com valores padrão
            print(f"Erro ao processar indicadores: {e}")
            processed.update(
                {
                    "patr_liq": 0.0,
                    "nr_cotas": 0.0,
                    "dy": 0.0,
                    "div_cota": 0.0,
                    "patr_cota": 0.0,
                    "pvp": 0.0,
                }
            )

        return processed
