import googlemaps
import os
import openpyxl
import pandas as pd
from coastLineChecker import is_on_brazilian_coast, load_coastline

def mapsJasonParser(db, dbIndex, result):
    '''
    This function gets the city and the state name from the Google Geocoding/Reverse Geocoding API response

    Parameters:
        db (Pandas DataFrame): Dataframe that is going to get the new information 
        dbIndex (Int):  Index of the dataframe
        result (Dictionary): Google API response
    '''

    tamResult = len(result[0]['address_components'])
    for numResu in range(tamResult):
        adressComponentType = result[0]['address_components'][numResu]['types'][0]
        match adressComponentType:
            case "administrative_area_level_2":
                city = result[0]['address_components'][numResu]['long_name']
                db.at[dbIndex, 'City'] = city
            case "administrative_area_level_1":
                state = result[0]['address_components'][numResu]['short_name']
                db.at[dbIndex, 'new_State'] = state

def mapsJasonParserLatLong(db, dbIndex, result, coastline):
    '''
    This function gets the Latitude and the Longitude from 
    the Google Geocoding/Reverse Geocoding API response and tells
    if the coordinates are on the coastline of Brazil or not

    Parameters:
        db (Pandas DataFrame): Dataframe that is going to get the new information 
        dbIndex (Int):  Index of the dataframe
        result (Dictionary): Google API response
        coastline (LineString): Brazil Coast Line
    '''

    lat = result[0]['geometry']['location']['lat']
    long = result[0]['geometry']['location']['lng']
    db.at[dbIndex, 'Latitude'] = lat
    db.at[dbIndex, 'Longitude'] = long
    db.at[dbIndex, 'onCoastLine'] = bool(is_on_brazilian_coast(lat, long, coastline)) 
    mapsJasonParser(db, dbIndex, result)

def searchStringBuilder(db, dbIndex):
    '''
    This Function makes a string using the geolocation and location collumns
    of the dataframe

    Parameters:
        db (Pandas Dataframe): Dataframe thar contains the geolocation and 
        location columns
        dbIndex (Int): Index of the dataframe

    Returns:
        str: String to be used in the google api
    '''

    citeBr = ""
    stringToSearch = ""

    dbGeoSearch = db.iloc[dbIndex]["Geolocation"]
    dbGeoSearchCheck = db.isnull().iloc[dbIndex]["Geolocation"]
    dbLocSearch = db.iloc[dbIndex]["Location"]
    dbLocSearchCheck = db.isnull().iloc[dbIndex]["Location"]

    if (not db.isnull().iloc[dbIndex]["State"]):
        citeBr =  ", " + db.iloc[dbIndex]["State"] + ", Brasil"
    else:
        citeBr = ", Brasil"

    if ((not dbGeoSearchCheck) and (not dbLocSearchCheck)):
        stringToSearch = dbGeoSearch + " " + dbLocSearch + citeBr
    elif(dbGeoSearchCheck and not dbLocSearchCheck):
        stringToSearch = dbLocSearch + citeBr
    elif(dbLocSearchCheck and not dbGeoSearchCheck):
        stringToSearch = dbGeoSearch + citeBr

    return stringToSearch



if __name__ == '__main__':
    
    # Initializing the MAPS API
    maps_key = os.environ['MAPS_API_KEY']
    gmaps = googlemaps.Client(key=maps_key)

    # Initialize coastline
    coastline = load_coastline("./shapeFiles/ne_10m_admin_0_countries.shp")

    # Reading the spreadsheet
    db = pd.read_excel("./Literature.xlsx")

    # Add the columns that we need if it doesnt already exist
    if ('Latitude' not in db.columns):
        db.insert(4, "Latitude", None)
    if ('Longitude' not in db.columns):
        db.insert(5, "Longitude", None)
    if ('onCoastLine' not in db.columns):
        db.insert(6, "onCoastLine", None)
    if ('City' not in db.columns):
        db.insert(7, "City", None)
    if ('new_State' not in db.columns):
        db.insert(8, "new_State", None)

    #Geocode API loop (this loop adds lat, lon, city, new_state)
    print("Wait a moment Running Geocode API .......... \n")
    stringToSearch = ""
    for num in range(len(db.index)):
        stringToSearch = searchStringBuilder(db, num)

        toBeFilled = (db.isnull().iloc[num]["Latitude"] or db.isnull().iloc[num]["Longitude"])

        if (stringToSearch == "" or (not toBeFilled)):
            continue
        else:
            geocode_result = gmaps.geocode(stringToSearch)
            if (len(geocode_result) != 0):
                mapsJasonParserLatLong(db, num, geocode_result, coastline)
            else:
                print(f"Error trying to find location on Google API: {stringToSearch}")
    print("Success!\n\n")

    # Reverse Geocode API loop (this loop adds city and new_state information for those lines that were empty)
    print("Wait a moment Running Reverse Geocode API ......... \n\n")
    for num in range(len(db.index)):

        # If City or State is empty we use reverse geocoding to get the data
        if (not (db.isnull().iloc[num]["Latitude"] or db.isnull().iloc[num]["Longitude"]) and db.isnull().iloc[num]["City"]):

            latSearch = db.iloc[num]["Latitude"]
            lonSearch = db.iloc[num]["Longitude"]

            reverse_geocode_result = gmaps.reverse_geocode((latSearch, lonSearch))

            if (len(reverse_geocode_result) != 0):
                mapsJasonParser(db, num, reverse_geocode_result)
            else:
                print(f"Error trying to find location on Google API: LAT:{latSearch} LON:{lonSearch}")
    print("Success\n\n")

    print("Process Completed!")
    db.to_excel("afterGoogleMapsAPI.xlsx");
     
        





        

