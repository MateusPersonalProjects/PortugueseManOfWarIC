import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import geodesic

def load_coastline(shapefile_path):
    """
    Loads a shapefile cotaining the Brazil's coastline

    Parameters:
        shapefile_path (str): Path to the archive.

    Returns:
        LineString: Brazil's coastline.
    """
    gdf = gpd.read_file(shapefile_path)
    
    # Filtrar para apenas a linha costeira do Brasil
    brazil = gdf[gdf['ADMIN'] == 'Brazil']  # Verifique o campo correto no seu shapefile
    coastline = brazil.geometry.unary_union
    
    # Garantir que a geometria seja um LineString
    if coastline.geom_type == 'MultiPolygon':
        coastline = coastline.boundary
    return coastline

def is_on_brazilian_coast(lat, lon, coastline, max_distance_km=40):
    """
    Verify if the coordinate (lat, lon) is closer to the Brazil's coastline.

    Parameters:
        lat (float): Latitude of the coordinate.
        lon (float): Longitude of the coordinate.
        coastline (LineString): Brazil's coastline.
        max_distance_km (float): Max distance to consider from the given coordinate to the coastline.

    Returns:
        bool: True if the given cordinate in on the coastline, False if it's not.
    """
    point = Point(lon, lat)
    nearest_point = coastline.interpolate(coastline.project(point))
    
    # Converte a distância de graus para quilômetros
    distance_km = geodesic((point.y, point.x), (nearest_point.y, nearest_point.x)).kilometers
    
    return distance_km <= max_distance_km

if __name__ == '__main__':
    coastline = load_coastline("./shapeFiles/ne_10m_admin_0_countries.shp")
    lat = -25.5469
    lon = -54.5882 

    is_on_brazilian_coast(lat, lon, coastline)
