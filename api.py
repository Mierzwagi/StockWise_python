from fastapi import FastAPI, File, UploadFile
import pandas as pd
import json
from io import BytesIO

app = FastAPI()

def clean_data(df, columns_to_drop, column_renames, fillna_dict=None, date_columns=None):
    df = df.drop(columns=columns_to_drop)
    if fillna_dict:
        df = df.fillna(fillna_dict)
    df = df.rename(columns=column_renames)
    if date_columns:
        for column in date_columns:
            df[column] = pd.to_datetime(df[column]).dt.date
    return df

def process_items(df):
    columns_to_drop = ['INVENTÁRIO', 'qnt', 'faltantes']
    column_renames = {
        'Nº inventário': 'Id',
        'Localização': 'Localizacao',
        'Denominação': 'Denominacao',
        'Incorporação em': 'Incorporacao em'
    }
    fillna_dict = {'Nº inventário': 0}
    date_columns = ['Incorporacao em']
    df = clean_data(df, columns_to_drop, column_renames, fillna_dict, date_columns)
    df['Id'] = df['Id'].astype('int64')
    return df

def process_rooms(df):
    column_renames = {
        'numero': 'Localizacao',
        'ambiente': 'Ambiente',
        'Responsável': 'Responsavel'
    }
    fillna_dict = {'Responsavel': "N/A"}
    return clean_data(df, [], column_renames, fillna_dict)

def aggregate_data(df_items, df_salas):
    df_resultado = pd.merge(df_items, df_salas, on='Localizacao', how='inner')
    groupLocalizacao = df_resultado.groupby('Localizacao')

    result = {}
    for localizacao, grupo in groupLocalizacao:
        items = grupo[["Id", "Denominacao", "Incorporacao em"]].to_dict("records")
        quantidade_inventario = int(grupo["Id"].count())
        sala = ", ".join(grupo["Ambiente"].unique())
        
        result[localizacao] = {
            "quantidade de itens": quantidade_inventario,
            "Sala": sala,
            "items": [
                {
                    "id": item["Id"],
                    "denominacao": item["Denominacao"],
                    "dataDeIncorporacao": item["Incorporacao em"],
                }
                for item in items
            ],
        }
    return result

@app.post("/process-xlsx/")
async def process_xlsx(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    # Ler e processar os arquivos XLSX
    df_items = pd.read_excel(BytesIO(await file1.read()))
    df_salas = pd.read_excel(BytesIO(await file2.read()))

    # Processamento dos dados
    df_items = process_items(df_items.copy())
    df_salas = process_rooms(df_salas.copy())
    
    # Agregar e gerar o resultado
    result = aggregate_data(df_items, df_salas)
    
    return json.loads(json.dumps(result, indent=2, ensure_ascii=False, default=str))
