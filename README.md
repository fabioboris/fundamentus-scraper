# Fundamentus Scraper

Uma ferramenta para obter e analisar dados financeiros de ações e FIIs do site [Fundamentus](https://www.fundamentus.com.br/).

## 📋 Descrição

Este projeto extrai dados fundamentalistas de ações e Fundos de Investimento Imobiliário (FIIs) do site Fundamentus, processa esses dados e permite salvá-los em formato Excel ou consultar indicadores específicos de um ativo. Ideal para análise de investimentos e tomadas de decisão baseadas em dados quantitativos.

## 🚀 Funcionalidades

- Extração automática de dados de todas as ações listadas no Fundamentus
- Extração automática de dados de todos os FIIs listados no Fundamentus
- Consulta rápida de indicadores específicos por ticker
- Exportação dos dados para arquivo Excel (com abas separadas para ações e FIIs)
- Interface de linha de comando simples e direta

## 📦 Pré-requisitos

- Python 3.8 ou superior
- Pacotes Python listados em `requirements.txt`:
  - beautifulsoup4
  - lxml
  - openpyxl
  - pandas
  - requests

## 🛠️ Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Como Usar

### Extrair todos os dados para um arquivo Excel

```bash
python -m app -o caminho/para/arquivo.xlsx
```

Se o parâmetro `-o` não for fornecido, os dados serão salvos em `downloads/fundamentus.xlsx`.

### Consultar indicadores de um ticker específico

```bash
python -m app -t PETR4
```

Este comando exibirá os principais indicadores para o ticker informado, incluindo:
- Cotação atual
- Dividend Yield (DY)
- Preço/Valor Patrimonial (P/VP)
- Data da última cotação

## 🔍 Exemplos

### Consultando um ticker específico:

```bash
python -m app -t ITUB4
```

Saída:
```
----------------------------------------
Ticker: ITUB4
Data da última cotação: 20/03/2025
Cotação: R$ 32.45
DY: 5.78%
P/VP: 1.54
----------------------------------------
```

### Extraindo para um arquivo personalizado:

```bash
python -m app -o analise/dados_fundamentalistas.xlsx
```

Saída:
```
Dados salvos com sucesso em: analise/dados_fundamentalistas.xlsx
```

## 📁 Estrutura do Projeto

```
├── app/
│   ├── __init__.py
│   ├── __main__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── extractor.py
│   │   ├── transformer.py
│   │   └── loader.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── fundamentus_service.py
│   └── ui/
│       ├── __init__.py
│       └── cli.py
├── tests/
├── requirements.txt
└── README.md
```

## 📊 Indicadores Disponíveis

### Ações
- Cotação
- P/L (Preço/Lucro)
- P/VP (Preço/Valor Patrimonial)
- Dividend Yield
- Margem EBIT
- Margem Líquida
- ROIC (Retorno sobre Capital Investido)
- ROE (Retorno sobre Patrimônio)
- E muitos outros

### FIIs
- Cotação
- Dividend Yield
- P/VP
- Vacância Média
- Quantidade de Imóveis
- Cap Rate
- E outros indicadores específicos para FIIs

## ⚠️ Limitações

- Os dados são obtidos do site Fundamentus e estão sujeitos à disponibilidade e precisão do mesmo
- O sistema não realiza atualização em tempo real, sendo necessário executar o comando novamente para obter dados atualizados
- A ferramenta não fornece análises ou recomendações de investimento

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para melhorias no código, novas funcionalidades ou correções de bugs.

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
