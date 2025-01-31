# ACTUALIZAR_TABLA_PRECIOS

Script de Python diseñado para actualizar los precios en un archivo CSV (archivo_a.csv) utilizando datos de un archivo Excel (archivo_b.xlsx).

***** ¡ATENCION! Crear un nuevo archivo_b que contenga solo la columna Cod. barra y la columna Precio  *****

### *** **Requisitos previos** ***

Antes de ejecutar el código, asegúrate de tener instalada la librería pandas, que es esencial para trabajar con archivos CSV, Excel y realizar manipulaciones de datos. 

Puedes instalarla utilizando el siguiente comando:

pip install pandas

### 1. **Cargar archivos**

archivo_a = pd.read_csv('archivo_a.csv')  # Archivo A en formato CSV
archivo_b = pd.read_excel('archivo_b.xlsx')  # Archivo B en formato Excel

- **`archivo_a.csv`**: Representa una tabla de datos con información principal (ej. lista de productos).
- **`archivo_b.xlsx`**: Contiene los nuevos precios que se deben usar para actualizar los productos en `archivo_a`.


### 2. **Limpieza de columnas clave (códigos de barras)**

archivo_a['GTIN, UPC, EAN, or ISBN'] = archivo_a['GTIN, UPC, EAN, or ISBN'].astype(str).str.strip()
archivo_b['Cod. Barra'] = archivo_b['Cod. Barra'].astype(str).str.strip()

- Se asegura de que las columnas de códigos de barras en ambos archivos sean cadenas de texto y elimina espacios innecesarios.
- Esto previene errores al comparar los códigos de barras.



### 3. **Normalización de precios en `archivo_b`**

 # Asegurar que sea texto para limpieza
archivo_b['Precio'] = archivo_b['Precio'].astype(str) 

# Eliminar comas
archivo_b['Precio'] = archivo_b['Precio'].str.replace(',', '')  

# Convertir a número
archivo_b['Precio'] = pd.to_numeric(archivo_b['Precio'], errors='coerce')  

- **Convertir a texto**: Se asegura de que los valores de la columna "Precio" en `archivo_b` sean tratados como cadenas para facilitar la limpieza.
- **Eliminar comas**: Si los precios están formateados con separadores de miles (`1,100.06`), se eliminan las comas.
- **Convertir a números**: Convierte los valores a un formato numérico. Si el valor no es convertible (por ejemplo, texto no válido), se convierte en `NaN`.



### 4. **Identificar precios no válidos**

precios_invalidos = archivo_b[archivo_b['Precio'].isna()]
if not precios_invalidos.empty:
    print("Advertencia: Se encontraron valores no válidos en el archivo_b:")
    print(precios_invalidos)

- Verifica si hay valores no válidos en la columna de precios después de la conversión.
- Imprime una advertencia con los detalles de los valores problemáticos.



### 5. **Eliminar duplicados en `archivo_b`**

archivo_b = archivo_b.drop_duplicates(subset=['Cod. Barra'])

- Se eliminan filas duplicadas basadas en la columna "Cod. Barra" para evitar conflictos durante la combinación.



### 6. **Renombrar columnas en `archivo_b`**

archivo_b.rename(columns={'Cod. Barra': 'GTIN, UPC, EAN, or ISBN'}, inplace=True)

- Cambia el nombre de la columna "Cod. Barra" en `archivo_b` para que coincida con el nombre en `archivo_a` (necesario para la combinación).



### 7. **Combinar archivos por código de barras**

archivo_a = archivo_a.merge(archivo_b[['GTIN, UPC, EAN, or ISBN', 'Precio']],
                            on='GTIN, UPC, EAN, or ISBN', how='left')

- Une ambos archivos basándose en la columna de códigos de barras (`GTIN, UPC, EAN, or ISBN`).
- Añade la columna "Precio" de `archivo_b` a `archivo_a`.



### 8. **Actualizar los precios en `archivo_a`**

archivo_a['Precio normal'] = archivo_a['Precio'].combine_first(archivo_a['Precio normal'])

- Actualiza la columna "Precio normal" de `archivo_a` con los valores de "Precio" de `archivo_b`.
- Si no hay un valor válido en "Precio", se conserva el precio original en `archivo_a`.



### 9. **Limpieza final y guardado**

archivo_a.drop('Precio', axis=1, inplace=True)  # Eliminar columna auxiliar 'Precio'
archivo_a.to_csv('archivo_a.csv', index=False)  # Guardar los cambios en archivo_a.csv

- Elimina la columna temporal "Precio" agregada durante el proceso de combinación.
- Sobrescribe el archivo `archivo_a.csv` con los precios actualizados.



### Resultado Final:
- Los precios en `archivo_a.csv` se actualizan solo si hay coincidencia con los códigos de barras de `archivo_b.xlsx`.
- Se mantienen los precios originales para los productos que no tienen coincidencia en `archivo_b`.
- Los precios no válidos o mal formateados en `archivo_b` no afectan el archivo final.
