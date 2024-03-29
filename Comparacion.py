import pandas as pd

# Se crea la lista de nombres de los países incluidos en el reporte para buscar su tabla correspondiente
total_paises = [
'Albania', 'Algeria', 'Angola', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahrain', 'Bangladesh',
'Barbados', 'Belgium', 'Benin', 'Bolivia', 'Bosnia and Herzegovina', 'Brazil', 'Brunei Darussalam',
'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Chad', 'Chile', 'China',
'Colombia', 'Congo, Democratic Rep.', 'Costa Rica', 'Côte d\'Ivoire', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark',
'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'Eswatini', 'Ethiopia', 'Finland', 'France', 'Gabon',
'Gambia, The', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Guatemala', 'Guinea', 'Haiti', 'Honduras', 'Hong Kong SAR',
'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Rep.', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan',
'Jordan', 'Kazakhstan', 'Kenya', 'Korea, Rep.', 'Kuwait', 'Kyrgyz Republic', 'Lao PDR', 'Latvia', 'Lebanon', 'Lesotho',
'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Mexico',
'Moldova', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand',
'Nicaragua', 'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines',
'Poland', 'Portugal', 'Qatar', 'Romania', 'Russian Federation', 'Rwanda', 'Saudi Arabia', 'Senegal', 'Serbia',
'Seychelles', 'Singapore', 'Slovak Republic', 'Slovenia', 'South Africa', 'Spain', 'Sri Lanka', 'Sweden', 'Switzerland',
'Taiwan, China', 'Tajikistan', 'Tanzania', 'Thailand', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Uganda', 'Ukraine',
'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Venezuela', 'Viet Nam', 'Yemen', 'Zambia',
'Zimbabwe'
]

# Lista de todos los países del APEC (Papua New Guinea no viene en el reporte)

APEC = ['Australia', 'Brunei Darussalam', 'Canada', 'Chile', 'China', 'Hong Kong SAR', 'Indonesia', 'Japan',
         'Korea, Rep.', 'Malaysia', 'Mexico', 'New Zealand', 'Peru', 'Philippines',
         'Russian Federation', 'Singapore', 'Taiwan, China', 'Thailand', 'United States', 'Viet Nam']

# Lista de todos los países del BRICS
BRICS = ["Brazil", "Russian Federation", "India", "China", "South Africa"]


# Ruta al archivo PDF The Global Competitiveness Report 2019
pdf_path = r'C:\Users\DELL\Desktop\Servicio Social\REPORTE.pdf'
dataframes_dict = {}
#Aquí se agrega la ruta donde se guardó el archivo Tablas_final
dataframes_dict = pd.read_pickle("Tablas_final.pkl")

'''
A apartir de aquí se hace la comparación entre México y el resto del APEC
'''
    
def comparar(pais,grupo,nombre_grupo):
    # Crear un nuevo diccionario paises_score solo con la columna 'Score'
    paises_score = {}
    for key, df in dataframes_dict.items():
        paises_score[key] = df['Score']
    
    # Crear un nuevo diccionario paises_score solo con la columna 'Value'
    paises_value = {}
    for key, df in dataframes_dict.items():
        paises_value[key] = df['Value']
        
        
    grupo = [key for key in grupo if key != pais]
    
    df_grupo_score = pd.DataFrame({key: paises_score[key] for key in grupo})
    df_grupo_score['Promedio'] = df_grupo_score.mean(axis=1)
    
    df_grupo_value = pd.DataFrame({key: paises_value[key] for key in grupo})
    df_grupo_value['Promedio'] = df_grupo_value.mean(axis=1)
    
    '''
Para comparar las diferencias de manera relativa y evitar el sesgo, se utiliza la siguiente fórmula para calcular la diferencia porcentual:

Diferencia Porcentual=|(|Columna1−Columna2|)/Promedio(Columna1,Columna2)|×100

Esta fórmula utiliza el promedio de los valores de ambas columnas como denominador, lo que ayuda a mitigar el sesgo.
    '''
    # Crear un DataFrame combinando los scores de México y el Grupo
    tabla_comparativa = pd.DataFrame({'Index component':dataframes_dict[pais].iloc[:, 0],
                                f'{pais} Value': paises_value[pais],
                                f'{nombre_grupo} Value': df_grupo_value['Promedio'],
                                'Difference Value %': abs((abs(paises_value[pais] - df_grupo_value['Promedio']) / ((paises_value[pais]+df_grupo_value['Promedio'])/2) * 100)),
                                f'{pais} Score': paises_score[pais],                          
                                f'{nombre_grupo} Score': df_grupo_score['Promedio'],
                                'Difference Score %': abs((abs(paises_score[pais] - df_grupo_score['Promedio']) / ((paises_score[pais]+df_grupo_score['Promedio'])/2) * 100))})
    tabla_comparativa.to_excel(f'tabla_comparativa{pais }vs{nombre_grupo}.xlsx', index=True)
    
    return tabla_comparativa

tabla_comparativa1=comparar('Azerbaijan', APEC,'APEC')
tabla_comparativa2=comparar('Mexico', BRICS,'BRICS')
tabla_comparativa3=comparar('United States', ["Brazil", "Russian Federation", "India", "China", "South Africa"],'BRICS')
tabla_comparativa4=comparar('United States', ["Russian Federation"],'Russia')




'''
Crear DF de todos los datos
paises_score = {}
for key, df in dataframes_dict.items():
    paises_score[key] = df['Score']

# Crear un nuevo diccionario paises_score solo con la columna 'Value'
paises_value = {}
for key, df in dataframes_dict.items():
    paises_value[key] = df['Value']
    

df_grupo_score = pd.DataFrame({f'{key} Score': paises_score[key] for key in dataframes_dict})
df_grupo_value = pd.DataFrame({f'{key} Value': paises_value[key] for key in dataframes_dict})

tabla_comparativa = pd.concat([dataframes_dict['Mexico'].iloc[:, 0], df_grupo_score, df_grupo_value], axis=1)
                                  
del df_grupo_score
del df_grupo_value

tabla_comparativa.to_excel('GCI_scores_values.xlsx', index=True)
'''











 