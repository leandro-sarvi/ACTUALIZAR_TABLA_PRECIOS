import pandas as pd

# Cargar archivo A (CSV) y archivo B (Excel)
archivo_a = pd.read_csv('archivo_a.csv')  # Archivo A en formato CSV
archivo_b = pd.read_excel('archivo_b.xlsx')  # Archivo B en formato Excel

# Limpiar columnas para evitar problemas de espacios
archivo_a['GTIN, UPC, EAN, or ISBN'] = archivo_a['GTIN, UPC, EAN, or ISBN'].astype(str).str.strip()
archivo_b['Cod. Barra'] = archivo_b['Cod. Barra'].astype(str).str.strip()

# Normalizar y convertir precios en archivo_b
archivo_b['Precio'] = archivo_b['Precio'].astype(str)  # Asegurar que sea texto para limpieza
archivo_b['Precio'] = archivo_b['Precio'].str.replace(',', '')  # Eliminar comas
archivo_b['Precio'] = pd.to_numeric(archivo_b['Precio'], errors='coerce')  # Convertir a número

# Identificar valores no válidos en archivo_b
precios_invalidos = archivo_b[archivo_b['Precio'].isna()]
if not precios_invalidos.empty:
    print("Advertencia: Se encontraron valores no válidos en el archivo_b:")
    print(precios_invalidos)

# Eliminar duplicados en archivo_b
archivo_b = archivo_b.drop_duplicates(subset=['Cod. Barra'])

# Renombrar columnas en archivo_b para que coincidan con archivo_a
archivo_b.rename(columns={'Cod. Barra': 'GTIN, UPC, EAN, or ISBN'}, inplace=True)

# Combinar datos basados en el código UPC
archivo_a = archivo_a.merge(archivo_b[['GTIN, UPC, EAN, or ISBN', 'Precio']],
                            on='GTIN, UPC, EAN, or ISBN', how='left')

# Actualizar los precios en archivo_a solo si hay coincidencia
archivo_a['Precio normal'] = archivo_a['Precio'].combine_first(archivo_a['Precio normal'])

# Eliminar columna auxiliar 'Precio'
archivo_a.drop('Precio', axis=1, inplace=True)

# Sobrescribir el archivo CSV original
archivo_a.to_csv('archivo_a.csv', index=False)

print("Archivo 'archivo_a.csv' actualizado correctamente.")

