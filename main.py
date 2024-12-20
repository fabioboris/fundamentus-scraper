import sys

import requests
from bs4 import BeautifulSoup
from math import sqrt


def obter_indicadores_fundamentus(ticker):
    url = f"http://www.fundamentus.com.br/detalhes.php?papel={ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
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


def main():
    if len(sys.argv) == 1:
        ticker = input("Digite o ticker do ativo: ").upper()
    else:
        ticker = sys.argv[1]

    data = obter_indicadores_fundamentus(ticker)

    dt_cotacao = data.get("Data últ cot", 0)
    cotacao = float(data.get("Cotação", 0))
    patr_liq = (
        float(data.get("Patrim Líquido", 0))
        if data.get("Patrim Líquido")
        else float(data.get("Patrim. Líq"))
    )
    nr_cotas = (
        float(data.get("Nro. Cotas", 0))
        if data.get("Nro. Cotas")
        else float(data.get("Nro. Ações", 0))
    )
    dy = float(data.get("Div. Yield", "0").strip("%")) / 100
    div_cota = cotacao * dy
    patr_cota = patr_liq / nr_cotas if nr_cotas != 0 else 0
    pvp = cotacao / patr_cota if patr_cota != 0 else 0

    print("-" * 40)
    print(f"Data da última cotação: {dt_cotacao}")
    print(f"Cotação: R$ {cotacao:.2f}")
    print(f"DY: {dy*100:.2f}%")
    print(f"P/VP: {pvp:.2f}")
    print("-" * 40)


if __name__ == "__main__":
    main()
