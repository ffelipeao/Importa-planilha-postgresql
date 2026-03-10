import geopandas as gpd
import numpy as np
from osgeo import gdal, osr
import os
from conexao import ConexaoBanco


conexao = ConexaoBanco().conectar()

# Definindo a consulta SQL para obter a geometria
schema = "shapes"+"."
tabela = "flona_zee"
consulta_sql = f"SELECT nome, ST_AsText(wkb_geometry) FROM {schema}{tabela}"

# Carregar dados com GeoPandas
gdf = gpd.read_postgis(consulta_sql, conexao, geom_col="wkb_geometry")

# Definindo o tamanho do raster
res_x = 100  # resolução em X
res_y = 100  # resolução em Y
xmin, ymin, xmax, ymax = gdf.total_bounds

# Calcular as dimensões do raster
largura = int((xmax - xmin) / res_x)
altura = int((ymax - ymin) / res_y)

# Criar o arquivo raster
output_raster = "output_raster.tif"
driver = gdal.GetDriverByName('GTiff')
raster = driver.Create(output_raster, largura, altura, 1, gdal.GDT_Byte)

# Configurar a projeção
spatial_ref = osr.SpatialReference()
spatial_ref.ImportFromEPSG(4674)  # SIRGAS 2000

# Definir a transformação geo para o raster
raster.SetGeoTransform((xmin, res_x, 0, ymax, 0, -res_y))
raster.SetProjection(spatial_ref.ExportToWkt())

# Criar a banda do raster e inicializar com 0
banda = raster.GetRasterBand(1)
banda.SetNoDataValue(0)
banda.Fill(0)

# Função para rasterizar as geometrias
for index, row in gdf.iterrows():
    geom = row['wkb_geometry']
    valor = 1  # Valor que deseja preencher no raster
    gdal.RasterizeLayer(raster, [1], geom, burn_values=[valor])

# Fechar e salvar
banda.FlushCache()
banda = None
raster = None

# Fechar a conexão
conn.close()
