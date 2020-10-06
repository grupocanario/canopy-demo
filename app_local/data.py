# --------------------
# Copyright (c) 2020 Grupo Canario

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# --------------------


import pandas as pd
import numpy as np
import json
from urllib.request import urlopen
import s3fs

# Codes shape Colombia for mapping
df_codes = pd.read_csv("https://raw.githubusercontent.com/melissamnt/code_utils/master/csv_department_codes.csv",
                   dtype={"cod": str})
df_codes['Code'] = df_codes['Code'].astype('str')
df_codes = df_codes.replace({'5': '05', '8': '08'})


# ALERTA ITEMS -----------------

# 1. Dataframe SECOP I & II items
df_raw_items = pd.read_csv("https://storage.googleapis.com/secop_data/secop_join_suministros_w_sobrecosto.csv")
df_items = df_raw_items.copy()

# Formatting with $ 
df_items['valor_del_contrato'] = df_items['valor_del_contrato'].map('${:,.0f}'.format)
df_items['precio_techo'] = df_items['precio_techo'].map('${:,.0f}'.format)
df_items['item_price'] = df_items['item_price'].map('${:,.0f}'.format)
# Formatting descripcion
df_items['item_description'] = df_items['item_description'].str.capitalize()
df_items['descripcion_del_proceso'] = df_items['descripcion_del_proceso'].str.capitalize()

df_items = df_items.rename(columns={
    'nombre_entidad': 'Nombre de la entidad',
    'departamento': 'Departamento',
    'ciudad': 'Municipio',
    'id_contrato': 'ID contrato',
    'descripcion_del_proceso': 'Descripcion del contrato',
    'tipo_de_contrato': 'Tipo de contrato',
    'modalidad_de_contratacion': 'Modalidad de contratacion',
    'proveedor_adjudicado': 'Proveedor adjudicado',
    'url': 'SECOP URL',
    'valor_del_contrato': 'Valor del contrato',
    'item_code': 'Código del item',
    'item_description': 'Descripción del item',
    'item_quantity': 'Cantidad del item',
    'item_price': 'Precio por item',
    'precio_piso': 'Precio minimo',
    'precio_techo': 'Precio maximo',
    'alarma_sobrecosto': 'Alerta de sobrecosto'
})

df_items = df_items[['Alerta de sobrecosto', 'Descripción del item', 'Nombre de la entidad', 'Departamento', 'Municipio', 'Proveedor adjudicado', 'Valor del contrato',
              'Cantidad del item', 'Precio por item', 'Precio maximo',
             'Descripcion del contrato', 
             'Tipo de contrato', 'SECOP URL']]
df_items['Alerta de sobrecosto'] = np.where(df_items['Alerta de sobrecosto']==True, 'Si', 'No')


entidades_items = df_items['Municipio'].unique()


# ALERTA TRANSPARENCIA -----------------
df_transparency = pd.read_csv('s3://proyectocanopy/alarma_transparencia.csv')

# Creating alarm variables
df_transparency['has_alarm'] = (df_transparency['reporta_items']!='SI_REPORTA')
# Filtering
df_transparency = df_transparency[df_transparency['has_alarm']]

# Formatting with $ 
df_transparency['valores'] = pd.to_numeric(df_transparency['valores'], errors='coerce')
df_transparency['valores'] = df_transparency['valores'].map('${:,.0f}'.format)
# Formatting descripcion
df_transparency['detalles'] = df_transparency['detalles'].str.capitalize()
# Formatting fechas with only date
df_transparency['date'] = pd.to_datetime(df_transparency['fechas']).dt.date
# Getting dates' month
df_transparency['month'] =pd.to_datetime(df_transparency['fechas']).dt.to_period("M")
# Capitalizing names of columns
df_transparency['municipio'] = df_transparency['municipio'].str.title()
df_transparency['departamento'] = df_transparency['departamento'].str.title()
df_transparency['contratista_name'] = df_transparency['contratista_name'].str.title()

df_transparency = df_transparency.rename(columns={
    'entidades': 'Nombre de la entidad',
    'departamento': 'Departamento',
    'municipio': 'Municipio',
    'date': 'Fecha del contrato',
    'detalles': 'Descripcion del contrato',
    'contratista_name': 'Proveedor adjudicado',
    'contratista_ids': 'ID Proveedor',
    'uri': 'SECOP URL',
    'valores': 'Valor del contrato',
    'month': 'Mes del contrato'
})

df_transparency = df_transparency[[ 'Fecha del contrato', 'Departamento', 'Municipio', 
                                   'Nombre de la entidad', 'Proveedor adjudicado', 
                                    'ID Proveedor', 'Valor del contrato',
                                     'Descripcion del contrato',  'SECOP URL']]
df_transparency = df_transparency.sort_values(by='Fecha del contrato', ascending=False)

# CONCENTRACION DE CONTRATISTAS -----------------

# 5. Dataframe SECOP I & II nombre de top 10 contratistas por depto
df_proov = pd.read_csv('s3://proyectocanopy/alarma_concentracion_valor_contratistas.csv')
df_proov = df_proov.drop_duplicates(subset=['contratista_ids', 'departamento_def'])
df_national_raw = df_proov.copy()  # Para global covid

# Only first 10 
df_proov['RN'] = df_proov.sort_values(['pct_def'], ascending=[False]) \
             .groupby(['departamento_def']) \
             .cumcount() + 1
df_proov = df_proov[df_proov['RN']<=10]

# Formatting with $ 
df_proov['val_contratista'] = df_proov['val_contratista'].map('${:,.0f}'.format)
# Formatting with %
df_proov_2 = df_proov.copy()
df_proov['pct_def'] = df_proov['pct_def'].map('{:.2f}'.format)
# Formatting with capitalization
df_proov['departamento_def'] = df_proov['departamento_def'].str.capitalize()
df_proov['contratista_name'] = df_proov['contratista_name'].str.title()

df_proov = df_proov.rename(columns={'contratista_ids':'Documento proveedor',
    'departamento_def': 'Departamento',
    'val_contratista': 'Valor de contratos',
    'pct_def': 'Pct de contratos',
    'contratista_name': 'Proveedor adjudicado'})

df_proov = df_proov[['Departamento', 'Proveedor adjudicado', 'Documento proveedor', 'Valor de contratos', 'Pct de contratos']]
df_proov = df_proov.sort_values(by='Pct de contratos', ascending=True)


# 4. Dataframe SECOP I & II concentracion top 10 contratistas por depto
df_proov_cum = df_proov_2.groupby(['departamento_def'])['pct_def'].sum().reset_index(name='pct_def')
df_proov_cum = df_proov_cum.rename(columns={'departamento_def':'departamento', 'pct_def': 'Pct acumulado proveedores'})

# Codes for map
df_proov_cum['Departamento_upper'] = df_proov_cum['departamento'].str.upper()
df_proov_cum['Departamento_upper'] = df_proov_cum['Departamento_upper'].replace({'QUINDIO': 'QUINDÍO'})
df_proov_cum = pd.merge(df_proov_cum, df_codes, left_on='Departamento_upper',  right_on='Departamento', how='left')
df_proov_cum = df_proov_cum.drop(['Departamento_upper', 'Departamento'], axis=1)
# Formatting
df_proov_cum['departamento'] = df_proov_cum['departamento'].str.title() 
df_proov_cum['Pct acumulado proveedores'] = np.round(df_proov_cum['Pct acumulado proveedores'], 2)
df_proov_cum = df_proov_cum.rename(columns={'departamento':'Departamento'})
df_proov_cum = df_proov_cum.sort_values(by='Pct acumulado proveedores', ascending=False)

df_proov_cum.loc[df_proov_cum['Departamento']=='San Andrés, Providencia y Santa Catalina', 'Departamento'] = 'San Andrés'


# FINANCIACIÓN DE CAMPAÑAS -----------------
financiacion = pd.read_csv('s3://proyectocanopy/alarma_financiacion.csv')

df_financiacion = financiacion.copy()

# Formatting with $ 
df_financiacion['valores'] = df_financiacion['valores'].map('${:,.0f}'.format)
# Formatting with capitalization
df_financiacion['detalles'] = df_financiacion['detalles'].str.capitalize()
df_financiacion['contratista_name'] = df_financiacion['contratista_name'].str.title()
df_financiacion['departamento_def'] = df_financiacion['departamento_def'].str.title()
df_financiacion['municipio_contrato'] = df_financiacion['municipio_contrato'].str.title()
df_financiacion['organizacion.politica'] = df_financiacion['organizacion.politica'].str.title()
df_financiacion['nombre.candidato'] = df_financiacion['nombre.candidato'].str.title()

# Formatting nulls of municipio
df_financiacion['municipio_contrato'] = df_financiacion['municipio_contrato'].fillna('')
# Formatting fechas with only date
df_financiacion['date'] = pd.to_datetime(df_financiacion['fechas']).dt.date
# Getting dates' month
df_financiacion['month'] =pd.to_datetime(df_financiacion['fechas']).dt.to_period("M")



df_financiacion = df_financiacion.rename(columns={
    'entidades': 'Nombre de la entidad',
    'departamento_def': 'Departamento contrato',
    'municipio_contrato': 'Municipio',
    'date': 'Fecha del contrato',
    'detalles': 'Descripcion del contrato',
    'contratista_name': 'Nombre Financiador',
    'contratista_ids': 'ID Financiador',
    'uri': 'SECOP URL',
    'valores': 'Valor del contrato',
    'valor': 'Valor del aporte',
    'month': 'Mes del contrato',
    'elegido': 'Candidato elegido',
    'organizacion.politica': 'Organización Política',
    'nombre.candidato': 'Nombre Candidato'
})


df_financiacion_final = df_financiacion[['Fecha del contrato', 'Departamento contrato',
                                   'Nombre de la entidad', 'Nombre Financiador', 
                                    'ID Financiador', 'Valor del contrato',
                                     'Descripcion del contrato', 'Valor del aporte',
                                 'Organización Política','Nombre Candidato', 'SECOP URL' ]]
df_financiacion_final = df_financiacion_final.sort_values(by='Fecha del contrato', ascending=False)

# Dataframe for graph
graph_f_df = df_financiacion.groupby(['Organización Política']).size().reset_index(name='Num contratos')
graph_f_df = graph_f_df.sort_values(by='Num contratos')
graph_f_df = graph_f_df.iloc[-11:-1,:]

del df_financiacion
del financiacion


# VISOR DE DATOS -----------------

# 3. Dataframe SECOP I & II map (number of COVID contracts)
# Grouping by number and sum of contracts
df_national_covid = df_national_raw.groupby(['departamento_def']).agg(
    num_contratos=('val_contratista', 'count'),
    sum_contratos=('val_contratista', 'sum'),
).reset_index()

# Formatting with capitalization
df_national_covid['departamento_def'] = df_national_covid['departamento_def'].str.capitalize()
# Upper for joins 
df_national_covid['Departamento_upper'] = df_national_covid['departamento_def'].str.upper()
df_national_covid['Departamento_upper'] = df_national_covid['Departamento_upper'].replace('QUINDIO', 'QUINDÍO')

# Joining with codes
df_national_covid = pd.merge(df_national_covid, df_codes, left_on='Departamento_upper',  right_on='Departamento', how='left')

# Rename colums
df_national_covid = df_national_covid.drop('Departamento', axis=1)
df_national_covid = df_national_covid.rename(columns={'departamento_def': 'Departamento',
                                                     'num_contratos': 'Num. contratos',
                                                     'sum_contratos': 'Total cuantía contratos'})
df_national_covid = df_national_covid[['Departamento', 'Num. contratos', 'Total cuantía contratos', 'Code']]



# SUMMARY ALL GRAPHS ------------------------
num_sobrecosto = len(df_items[df_items['Alerta de sobrecosto']=='Si'])
num_transparencia = len(df_transparency)
num_financiacion = len(df_financiacion_final)

df_summary = pd.DataFrame.from_dict({'Alerta':['Sobrecosto', 'Transparencia', 'Financiación'], 'Número de alertas':[num_sobrecosto, num_transparencia, num_financiacion]})