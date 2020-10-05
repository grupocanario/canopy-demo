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

# VISOR DE DATOS -----------------

# 3. Dataframe SECOP I & II map (number of COVID contracts)
df_raw_covid = pd.read_csv("https://raw.githubusercontent.com/carlosacaro/dataton_ocp/master/secop_all_is_covid.csv")

df_covid = df_raw_covid.copy()
df_national_covid = df_covid.groupby('departamento').size().reset_index(name='Num. contratos')
df_national_covid = df_national_covid.rename(columns={'departamento':'Departamento'})
df_national_covid['Departamento_upper'] = df_national_covid['Departamento'].str.upper()

df_codes = pd.read_csv("https://raw.githubusercontent.com/melissamnt/code_utils/master/csv_department_codes.csv",
                   dtype={"cod": str})
df_codes['Code'] = df_codes['Code'].astype('str')
df_codes = df_codes.replace({'5': '05', '8': '08'})
df_national_covid = pd.merge(df_national_covid, df_codes, left_on='Departamento_upper',  right_on='Departamento', how='left')
df_national_covid = df_national_covid.rename(columns={'Departamento_x':'Departamento'}).drop(['Departamento_upper', 'Departamento_y'], axis=1)



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

# # 2. Dataframe SECOP I & II transparency
# df_raw_transparency = pd.read_csv("https://storage.googleapis.com/secop_data/secop_2_covid_singleitem.csv")
# df_transparency = df_raw_transparency.copy()

# # Formatting with $ 
# df_transparency['valor_del_contrato'] = df_transparency['valor_del_contrato'].map('${:,.0f}'.format)
# # Formatting descripcion
# df_transparency['descripcion_del_proceso'] = df_transparency['descripcion_del_proceso'].str.capitalize()

# df_transparency = df_transparency.rename(columns={
#     'nombre_entidad': 'Nombre de la entidad',
#     'departamento': 'Departamento',
#     'ciudad': 'Municipio',
#     'id_contrato': 'ID contrato',
#     'descripcion_del_proceso': 'Descripcion del contrato',
#     'tipo_de_contrato': 'Tipo de contrato',
#     'modalidad_de_contratacion': 'Modalidad de contratacion',
#     'proveedor_adjudicado': 'Proveedor adjudicado',
#     'url': 'SECOP URL',
#     'valor_del_contrato': 'Valor del contrato',
#     'items_per_contract': 'Items por contrato'
# })
# fin del comentarios

# df_transparency = df_transparency[['Nombre de la entidad', 'Departamento', 'Municipio', 'Proveedor adjudicado', 'Valor del contrato',
#              'Descripcion del contrato',  'SECOP URL']]




# CONCENTRACION DE CONTRATISTAS -----------------

# 4. Dataframe SECOP I & II concentracion top 10 contratistas por depto
df_raw_proov_cum = pd.read_csv("https://raw.githubusercontent.com/carlosacaro/dataton_ocp/master/cum_dept_valor.csv")
df_proov_cum = df_raw_proov_cum.rename(columns={'0':'departamento', '1': 'Pct proveedores'})
df_proov_cum = df_proov_cum.drop('Unnamed: 0', axis=1)

df_proov_cum = df_proov_cum.sort_values(by='Pct proveedores', ascending=True)
# Codes for map
df_proov_cum['Departamento_upper'] = df_proov_cum['departamento'].str.upper()
df_proov_cum = pd.merge(df_proov_cum, df_codes, left_on='Departamento_upper',  right_on='Departamento', how='left')
df_proov_cum = df_proov_cum.drop(['Departamento_upper', 'Departamento'], axis=1)
df_proov_cum = df_proov_cum.rename(columns={'departamento':'Departamento'})

df_proov_cum.loc[df_proov_cum['Departamento']=='San Andrés, Providencia y Santa Catalina', 'Departamento'] = 'San Andrés'

# 5. Dataframe SECOP I & II nombre de top 10 contratistas por depto
df_raw_proov = pd.read_csv("https://raw.githubusercontent.com/carlosacaro/dataton_ocp/master/prov_dept_valor.csv")

df_proov = df_raw_proov.copy()
# Formatting numbers
df_proov['valor_del_contrato'] = df_proov['valor_del_contrato'].map('${:,.0f}'.format)
df_proov['cumpercentage'] = df_proov['cumpercentage'].map('{:.1f}%'.format)

df_proov = df_proov.rename(columns={'documento_proveedor':'Documento proveedor',
    'departamento': 'Departamento',
    'valor_del_contrato': 'Valor del contrato',
    'cumpercentage': 'Pct acumulado de contratos',
    'tipodocproveedor': 'Tipo documento proveedor',
    'proveedor_adjudicado': 'Proveedor adjudicado'})

df_proov = df_proov.drop('Unnamed: 0', axis=1)



