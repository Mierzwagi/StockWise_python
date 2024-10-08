# StockWise_python

## Funcionalidades

- Upload de dois arquivos XLSX.
- Limpeza e transformação dos dados para um formato específico.
- Agregação dos dados com base na localização.
- Retorno dos dados processados em formato JSON.

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e de alta performance para a construção da API.
- **Pandas**: Biblioteca poderosa para manipulação e análise de dados.
- **Uvicorn**: Servidor ASGI para rodar a aplicação FastAPI.
- **openpyxl**: Biblioteca para ler e escrever arquivos Excel (XLSX).
- **python-multipart**: Necessário para lidar com uploads de arquivos na API.

## Requisitos

- Python 3.8+
- Bibliotecas listadas em `requirements.txt`

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```
## Executando a API

1. **Execute a aplicação:**
    ```bash
    uvicorn api:app --reload
    ```

2. **Acesse a API:**
    Abra o navegador e acesse http://127.0.0.1:8000/docs para visualizar a documentação interativa gerada automaticamente pelo FastAPI.