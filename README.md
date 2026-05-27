# Homicídios Mundiais (UNODC) — Análise e Previsão (2013–2026)

Este projeto usa o dataset **UNODC – Intentional Homicide Victims** para analisar homicídios por país e gerar **previsões para 2023–2026** usando **Regressão Linear**.

## Participantes

- José Ericson Silveira Teófilo
- Igor da Silva Pierre
- Glória Maria Mesquita Furtado
- Pedro Carolino Neto
- Jeferson Rodrigo Silva de Mesquita
- Antonio Lucas Damasceno Melo

Você tem duas formas de explorar o trabalho:

- `AP01_Homicidios_COMPLETO.ipynb`: notebook do Google Colab com a análise completa (exploração dos dados + regressões).
- `dataapp.py`: aplicação web (Streamlit) para interagir com as previsões por país e comparar até 5 países.

## Arquivos principais

- `dataapp.py`: Streamlit app com previsão por país (2013–2022 → 2023–2026).
- `AP01_Homicidios_COMPLETO.ipynb`: notebook do Colab (inclui células de instalação, carga do Excel e gráficos).
- `data_cts_intentional_homicide.xlsx`: planilha com as duas abas do dataset (a análise e o app dependem desse arquivo).

## Fonte dos dados

- UNODC (UNODC Data Portal): [dp-intentional-homicide-victims](https://dataunodc.un.org/dp-intentional-homicide-victims)
- Período no dataset usado pela análise: **2013 a 2022**

---

## Como usar o Notebook (export do Colab)

1. Abra `AP01_Homicidios_COMPLETO.ipynb` em **Google Colab** (recomendado).
   - Observação: o notebook usa `google.colab.files.upload()`, então rodar local (Jupyter “puro”) exige adaptar as células de upload e o `ARQUIVO`.
2. Faça upload do arquivo `data_cts_intentional_homicide.xlsx` quando o script solicitar (`files.upload()`).
3. Garanta que o Excel está no caminho esperado por `ARQUIVO`:
   - O notebook define `ARQUIVO = '/content/sample_data/data_cts_intentional_homicide.xlsx'`.
   - No Colab, `files.upload()` normalmente salva o arquivo em `/content/` (e não automaticamente em `sample_data/`).
   - Portanto, antes de continuar, faça 1 destes:
     - mover o arquivo para `sample_data/` (mantendo o `ARQUIVO` como está);
     - ou alterar `ARQUIVO` para apontar para o caminho real do arquivo que você acabou de enviar.
4. Execute o arquivo **de cima para baixo**.

O notebook realiza:
- carga das duas abas do Excel (`data_cts_intentional_homicide` e `data_cts_homicide_reg_estimates`);
- exploração e tratamento dos dados;
- análise com estatística descritiva e gráficos;
- regressão por país para prever **2023–2026**, incluindo métricas de erro e visualizações.

Dependências (para rodar no Colab):
- O notebook já executa uma célula de instalação para `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly` e `openpyxl`.
- A seção de regressão usa `scikit-learn` (no Colab ele normalmente já está disponível). Se você adaptar o notebook para rodar local, instale também `scikit-learn`.

## Como usar o Data App (Streamlit)

1. Pré-requisito: tenha o Python instalado.
2. Mantenha `data_cts_intentional_homicide.xlsx` **na mesma pasta** do `dataapp.py`.
3. (Ubuntu/Debian) Crie e ative um ambiente virtual (evita o erro `externally-managed-environment`):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Instale as dependências (todas as versões estão fixadas em `requirements.txt`):

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

5. Rode o app:

```bash
streamlit run dataapp.py
```

6. Abra a URL exibida no terminal.
7. Use a barra lateral para:
   - escolher um país para visualizar a curva histórica (2013–2022) e a previsão (2023–2026);
   - selecionar até 5 países para o comparativo das previsões.

Observações do modelo implementado em `dataapp.py`:
- lê a primeira aba do Excel (`sheet_name=0`);
- filtra para `Indicator="Victims of intentional homicide"` e dimensões “Total”/“Total”, unidade “Counts”;
- treina uma regressão linear por país usando `Year` → `VALUE`;
- calcula métricas (R², MAE, RMSE, erro máximo) e prevê 2023–2026 (valores negativos são truncados para `0`).

---

## Se der erro (check rápido)

- Se o notebook não achar o Excel: verifique o `ARQUIVO` (path no Colab).
- Se o app do Streamlit não carregar: confirme que o arquivo `data_cts_intentional_homicide.xlsx` está no mesmo diretório e com esse nome.

