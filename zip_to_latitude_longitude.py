import pandas
import os

###################################

#this script allowed us to map 11,000+ US zip codes to their respective latitude/longitude coordinates.

#INPUT FILES
#"zip_codes.txt" is a file that contains all unique zip codes in our dataset (1 zip code per line)
#"zip_to_lat_lon_North_America.csv" is a file that maps all US zip codes to their respective geocoordinates (latitude/longitude coordinates)

#OUTPUT FILES
#"geo_coordinates.csv" contains all unique zip codes in our dataset mapped with their respective latitude/longitude coordinates
#"missing_values.txt" contains the zip codes in our dataset that haven't been mapped to any latitude/longitude coordinates (those are not existing zip codes)

###################################

#dataframe in which are documented the latitude/longitude coordinates associated with each US zip code 
#we retrieved the datafile here: https://www.listendata.com/2020/11/zip-code-to-latitude-and-longitude.html
dataframe = pandas.read_csv(filepath_or_buffer="zip_to_lat_lon_North_America.csv",
                                sep=",",
                                dtype=object,
                                usecols=["country code", "postal code", "latitude", "longitude"],
                                encoding='utf8',
                                engine="c")

#.txt file in which are documented all unique zip codes in our dataset (1 zip code per line)
with open("zip_codes.txt", "r") as opening:
    zip_list = opening.read().split("\n")

final_list = "zip_code;latitude;longitude;geo_coordinates"

#here we map each unique zip code of interest to its latitude/longitude coordinates by searching for them in the "zip_to_lat_lon_North_America.csv" file
for i, zip_code in enumerate(zip_list):
    print("{}/{}".format(str(i), str(len(zip_list))))
    try:
        if zip_code[0] == "0":
            zip_code = zip_code[1:]
        country_df = dataframe.loc[dataframe["country code"] == "US"]
        zip_df = country_df.loc[country_df["postal code"] == zip_code]
        latitude = str(zip_df["latitude"][list(zip_df.index)[0]])
        longitude = str(zip_df["longitude"][list(zip_df.index)[0]])
        geo_coordinates = "{},{}".format(latitude, longitude)
        final_list += "\n{};{};{};{}".format(zip_code, latitude, longitude, geo_coordinates)
    except:
    #case where the zip code of interest is not documented in the "zip_to_lat_lon_North_America.csv" file
        final_list += "\n{};NA;NA;NA".format(zip_code)
        with open("missing_values.txt", "a") as opening:
            opening.write("{}\n".format(zip_code))

with open("geo_coordinates.csv", "w") as opening:
    opening.write(final_list)

os.system("pause")