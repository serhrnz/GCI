import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output, Markdown

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
    tabla_comparativa.to_excel(f'tabla_comparativa{pais }vs{nombre_grupo}.xlsx', index=False)
    print(tabla_comparativa)
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
pais = dropdown_pais.value
grupo = []
nombre_grupo = 'Grupo'
def ejecutar_comparacion(b):
    # Aquí utilizas los valores actuales para llamar a comparar
    resultado = comparar(pais, grupo, nombre_grupo)
# Función para mostrar los widgets adicionales
def mostrar_elementos(b):

    cantidad = entrada_cantidad.value
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
print("Seleccione el país elegido para su comparación:")
display(dropdown_pais)
print("Ingrese el número de países que tendrá el grupo a comparar:")
display(entrada_cantidad)
print("Presione 'Elegir' para seleccionar los países del grupo:")
display(boton_elegir, contenedor_elementos, salida)
