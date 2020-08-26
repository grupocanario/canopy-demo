import pandas as pd
import numpy as np
import json
from urllib.request import urlopen

# VISOR DE DATOS -----------------

# 3. Dataframe SECOP I & II map (number of COVID contracts)
df_raw_covid = pd.read_csv("https://raw.githubusercontent.com/carlosacaro/dataton_ocp/master/secop_all_is_covid.csv")

df_covid = df_raw_covid.copy()
df_national_covid = df_covid.groupby('departamento').size().reset_index(name='Numero de contratos COVID')
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

df_items = df_items[['Alerta de sobrecosto', 'Descripción del item', 'Nombre de la entidad', 'Departamento', 'Municipio', 'Proveedor adjudicado', 'Valor del contrato', 'Código del item',
              'Cantidad del item', 'Precio por item', 'Precio minimo', 'Precio maximo',
             'Descripcion del contrato', 'ID contrato',
             'Tipo de contrato', 'Modalidad de contratacion',  'SECOP URL']]
df_items['Alerta de sobrecosto'] = np.where(df_items['Alerta de sobrecosto']==True, 'Si', 'No')
df_items['SECOP URL'] = '[Link](' + df_items['SECOP URL'] + ')'


entidades_items = df_items['Municipio'].unique()


# ALERTA TRANSPARENCIA -----------------

# 2. Dataframe SECOP I & II transparency
df_raw_transparency = pd.read_csv("https://storage.googleapis.com/secop_data/secop_2_covid_singleitem.csv")
df_transparency = df_raw_transparency.copy()

# Formatting with $ 
df_transparency['valor_del_contrato'] = df_transparency['valor_del_contrato'].map('${:,.0f}'.format)
# Formatting descripcion
df_transparency['descripcion_del_proceso'] = df_transparency['descripcion_del_proceso'].str.capitalize()

df_transparency = df_transparency.rename(columns={
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
    'items_per_contract': 'Items por contrato'
})

df_transparency = df_transparency[['Nombre de la entidad', 'Departamento', 'Municipio', 'Proveedor adjudicado', 'Valor del contrato',
             'Descripcion del contrato',  'SECOP URL']]




# CONCENTRACION DE CONTRATISTAS -----------------

# 4. Dataframe SECOP I & II concentracion top 10 contratistas por depto
df_raw_proov_cum = pd.read_csv("https://raw.githubusercontent.com/carlosacaro/dataton_ocp/master/cum_dept_valor.csv")
df_proov_cum = df_raw_proov_cum.rename(columns={'0':'Departamento', '1': 'Pct proveedores'})
df_proov_cum = df_proov_cum.drop('Unnamed: 0', axis=1)
df_proov_cum = df_proov_cum.sort_values(by='Pct proveedores', ascending=True)

# 5. Dataframe SECOP I & II nombre de top 10 contratistas por depto
df_raw_proov = pd.read_csv("https://raw.githubusercontent.com/carlosacaro/dataton_ocp/master/prov_dept_valor.csv")
df_proov = df_raw_proov.rename(columns={'documento_proveedor':'Documento proveedor',
    'departamento': 'Departamento',
    'valor_del_contrato': 'Valor del contrato',
    'tipodocproveedor': 'Tipo documento proveedor',
    'proveedor_adjudicado': 'Proveedor adjudicado'})
df_proov = df_proov.drop('Unnamed: 0', axis=1)



