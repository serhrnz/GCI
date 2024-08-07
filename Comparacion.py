import pandas as pd
import ipywidgets as widgets
from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np

# Se crea la lista de nombres de los países incluidos en el reporte para buscar su tabla correspondiente
opciones_pais = [
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


dataframes_dict = {}
#Aquí se agrega la ruta donde se guardó el archivo Tablas_final
dataframes_dict = pd.read_pickle("https://github.com/serhrnz/GCI/raw/main/Tablas_final.pkl")

'''
A apartir de aquí se hace la comparación entre México y el resto del APEC
'''
def plot_radar_chart(tabla_comparativa):
    keyword = "pillar"
    # Filtrar las filas por los índices que contienen 'keyword'
    filtered_labels = tabla_comparativa['Index component'].str.contains(keyword)
    filtered_data = tabla_comparativa[filtered_labels]
    num_vars = len(filtered_data)
        
    # Preparar las etiquetas y ángulos
    original_labels = filtered_data['Index component'].tolist()
    original_labels = [label.split(': ',)[1] for label in original_labels]
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Completar el ciclo para el gráfico radar

    # Completar las series para que el gráfico radar sea un ciclo cerrado
    pais_scores = filtered_data[f'{pais} Score'].tolist()
    pais_scores += pais_scores[:1]
    grupo_scores = filtered_data[f'{nombre_grupo} Score'].tolist()
    grupo_scores += grupo_scores[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # Rellenar el área del gráfico radar
    ax.fill(angles, pais_scores, alpha=0.1, color='blue', label=pais)
    ax.fill(angles, grupo_scores, alpha=0.1, color='red', label=nombre_grupo)
    
    # Trazar las líneas de los datos
    ax.plot(angles, pais_scores, color='blue', linewidth=2, linestyle='solid')
    ax.plot(angles, grupo_scores, color='red', linewidth=2, linestyle='solid')
    
    # Ajustar el rango del eje radial
    ax.set_ylim(0, 100)  # Ajustar el rango del eje radial según tus datos específicos
    
    # Configurar las etiquetas de los ángulos
    ax.set_thetagrids(np.degrees(angles[:-1]), original_labels)  # Excluir el último ángulo repetido
    
    # Añadir título y leyenda
    ax.set_title(f'Comparación de los 12 pilares del GCI 4.0 2019 entre {pais} y {nombre_grupo}', y=1.08)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
    plt.show()

def comparar(country,group,nombre_group):
    # Crear un nuevo diccionario countries_score solo con la columna 'Score'
    countries_score = {}
    for key, df in dataframes_dict.items():
        countries_score[key] = df['Score']
    
    # Crear un nuevo diccionario countries_score solo con la columna 'Value'
    countries_value = {}
    for key, df in dataframes_dict.items():
        countries_value[key] = df['Value']
        
        
    group = [key for key in group if key != country]
    
    df_group_score = pd.DataFrame({key: countries_score[key] for key in group})
    df_group_score['Promedio'] = round(df_group_score.mean(axis=1),2)
    
    df_group_value = pd.DataFrame({key: countries_value[key] for key in group})
    df_group_value['Promedio'] = round(df_group_value.mean(axis=1),2)
    
    '''
Para comparar las diferencias de manera relativa y evitar el sesgo, se utiliza la siguiente fórmula para calcular la diferencia porcentual:

Diferencia Porcentual=|(|Columna1−Columna2|)/Promedio(Columna1,Columna2)|×100

Esta fórmula utiliza el promedio de los valores de ambas columnas como denominador, lo que ayuda a mitigar el sesgo.
    '''
    # Crear un DataFrame combinando los scores de México y el Grupo
    tabla_comparativa = pd.DataFrame({'Index component':dataframes_dict[country].iloc[:, 0],
                                f'{country} Value': countries_value[country],
                                f'{nombre_group} Value': df_group_value['Promedio'],
                                'Difference Value %': round(abs((abs(countries_value[country] - df_group_value['Promedio']) / ((countries_value[country]+df_group_value['Promedio'])/2) * 100)),2),
                                f'{country} Score': countries_score[country],                          
                                f'{nombre_group} Score': df_group_score['Promedio'],
                                'Difference Score %': round(abs((abs(countries_score[country] - df_group_score['Promedio']) / ((countries_score[country]+df_group_score['Promedio'])/2) * 100)),2)})
    tabla_comparativa.to_excel(f'{country }vs{nombre_group}.xlsx', index=False)
    print(f"Se ha generado el archivo Excel con la tabla comparativa entre {pais} y {nombre_grupo}.\nPara descargarlo, revise la sección 'Archivos' a la izquierda de la pantalla haciendo clic en el icono en forma de folder.\nDespués, de clic en los tres puntos y luego en 'Descargar'.")     
    plot_radar_chart(tabla_comparativa)    
    return tabla_comparativa



# Dropdown para país
dropdown_pais = widgets.Dropdown(
    options=opciones_pais,
    description='País:',
    disabled=False,
)

# Campo de entrada para especificar la cantidad de elementos en el grupo
entrada_cantidad = widgets.BoundedIntText(
    value=1,
    min=1,
    max=len(opciones_pais),
    description='Cantidad:',
    disabled=False
)

# Campo de texto para asignar el nombre del grupo
entrada_nombre_grupo = widgets.Text(
    value='',
    placeholder='Ingrese el nombre del grupo',
    description='Nombre:',
    disabled=False
)
# Botón para elegir la cantidad y mostrar los desplegables
boton_elegir = widgets.Button(description="Elegir")

# Botón para agregar al grupo los elementos seleccionados
boton_agregar_grupo = widgets.Button(description="Agregar al grupo")

# Botón para comparar el país base con el grupo seleccionado
boton_comparar = widgets.Button(description="Comparar")

# Contenedor para los widgets adicionales y salida
contenedor_elementos = widgets.VBox([])
salida = widgets.Output()

# Variable para almacenar el grupo de elementos seleccionados
pais = 'Mexico'
grupo = []
nombre_grupo = 'Grupo'

def ejecutar_comparacion(b):
    # Aquí utilizas los valores actuales para llamar a comparar
    comparar(pais, grupo, nombre_grupo)
    
# Función para mostrar los widgets adicionales
def mostrar_elementos(b):
    global pais  # Esto es importante para que cambie la variable global
    cantidad = entrada_cantidad.value
    pais = dropdown_pais.value 
    nuevos_widgets = []
    for i in range(cantidad):
        nuevos_widgets.append(
            widgets.Dropdown(
                options=opciones_pais,
                description=f'Elemento {i + 1}:',
                disabled=False,
            )
        )

    contenedor_elementos.children = nuevos_widgets


    print('Establezca el nombre del grupo (por ejemplo: "Grupo A")')
    display(entrada_nombre_grupo,boton_agregar_grupo)


# Función para agregar al grupo los elementos seleccionados
def agregar_al_grupo(b):
    global grupo, nombre_grupo
    grupo = [dropdown.value for dropdown in contenedor_elementos.children]  # Recopilar valores de los dropdowns (excepto el botón)
    nombre_grupo = entrada_nombre_grupo.value  # Guardar el nombre del grupo

    print("País a comparar:", pais)
    print("Grupo agregado:", grupo)
    print("Nombre del grupo:", nombre_grupo)
    display(boton_comparar)

# Asociar funciones con los botones
boton_elegir.on_click(mostrar_elementos)
boton_agregar_grupo.on_click(agregar_al_grupo)
boton_comparar.on_click(ejecutar_comparacion)

# Mostrar la interfaz inicial
print("\nSeleccione el país elegido para su comparación:")
display(dropdown_pais)
print("Ingrese el número de países que tendrá el grupo a comparar:")
display(entrada_cantidad)
print("Presione 'Elegir' para seleccionar los países del grupo:")
display(boton_elegir, contenedor_elementos, salida)
