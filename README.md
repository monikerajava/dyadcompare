# DyadCompare

Aplicação web para comparar arquivos de texto em uma interface de duas colunas, inspirada no fluxo de trabalho do Beyond Compare.

## Recursos

- Comparação lado a lado, unificada ou em lista de alterações.
- Realce de linhas adicionadas, removidas e alteradas, com destaque de caracteres nas substituições lado a lado.
- Opções para ignorar espaços em branco, diferenças entre maiúsculas e minúsculas e linhas vazias.
- Navegação pelas diferenças e controle das linhas de contexto exibidas.
- Resumo das alterações e suporte a UTF-8 e Windows-1252.
- Tema claro e escuro.
- Limite de 50 MB por arquivo.

O foco atual são arquivos de texto. Arquivos binários e comparação de pastas ainda não são suportados.

## Publicar no Streamlit Community Cloud

1. Crie um repositório no GitHub e envie os arquivos deste projeto para a raiz dele. Inclua a pasta `.streamlit` e o arquivo `requirements.txt`.
2. Entre em [share.streamlit.io](https://share.streamlit.io/) com sua conta e conecte o GitHub.
3. Escolha **Create app** e informe o repositório, a branch e `app.py` como arquivo principal.
4. Nas opções avançadas, selecione Python 3.12 e clique em **Deploy**.
5. Quando a implantação terminar, compartilhe o endereço `*.streamlit.app` gerado.

Na versão online, os arquivos enviados chegam ao servidor para processamento. A aplicação não possui banco de dados nem grava arquivos enviados em disco; mesmo assim, não envie conteúdo confidencial.

Consulte o [guia oficial de implantação](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) para detalhes de configuração da conta e do repositório.

## Executar localmente

Requer Python 3.11 ou superior.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Testes

```powershell
python -m unittest discover -s tests -v
```
