
import pandas as pd
from geopy.extra.rate_limiter import RateLimiter
import geopy
import time
import folium
import matplotlib.colors as mcolors
from datetime import datetime

easement_df = pd.read_excel("Easement List.xlsx")
easement_df = easement_df.fillna("")
easement_df.columns = easement_df.columns.str.replace(" ","")



today = datetime.now().strftime("%Y-%m-%d")


locator = geopy.Nominatim(user_agent= "myGeocoder")


color_list =['#acc2d9','#0a5f38','#fe4b03','#952e8f',
'#08787f',
'#ff63e9','#c48efd','#6b7c85',
'#1d5dec','#c87f89','#cb6843','#214761','#ba9e88']

output_df = pd.DataFrame()
error_df = pd.DataFrame()


for idx, row in easement_df.iterrows():
    this_property = row['Property'] 
    this_number = row['Number']
    this_neighborhood = row["Neighborhood"] + " " + row["Group"]
    details =""
    if ',' in this_property:
        line_split = this_property.split(',')
        this_property = line_split[1].strip() + ' ' + line_split[0].strip()
    if '-' in str(this_number):
        this_number = this_number.split("-")[0]
        this_number = this_number.strip()
        details ="Range"
    this_address = str(this_number) + " " + this_property + " Richmond, VA"
    this_loc = locator.geocode(this_address)
    try:
        row['lat'] = this_loc.latitude
        row['lon'] = this_loc.longitude
        new_data = [this_number, this_address,this_neighborhood,this_loc.latitude,this_loc.longitude,details]
        new_row = pd.DataFrame([new_data],columns = ["Number","Property","Neighborhood","lat","lon","details"])
        output_df = pd.concat([output_df,new_row])
        print(this_address + " added, sleeping for half second")
        time.sleep(0.5)
    
    except:
        print("Error at position " + str(idx))
        err_data = [this_number, this_address,row['Neighborhood'], row['Group']]
        err_row = pd.DataFrame([err_data], columns=["Number","Property","Neighborhood","Group"])

list_of_neighborhoods =pd.unique(easement_df['Neighborhood'])
color_dict = {}
used_colors =[]
for this_neighborhood in list_of_neighborhoods:
    for key in mcolors.TABLEAU_COLORS:
        if key not in used_colors:
            color_dict[this_neighborhood] = mcolors.TABLEAU_COLORS[key]
            used_colors.append(key)
            break


list_of_neighborhoods =pd.unique(output_df['Neighborhood'])
color_dict = {}
used_colors =[]
for this_neighborhood in list_of_neighborhoods:
    for this_color in color_list:
        if this_color not in used_colors:
            color_dict[this_neighborhood] = this_color
            used_colors.append(this_color)
            break

output_df['color']= output_df['Neighborhood'].map(color_dict)
output_df.to_csv(today + "_output_data.csv")

if len(error_df) > 0:
    error_df.to_csv(today + "_errors.csv")




map1 = folium.Map(
    location=[37.538307530016894,
              -77.436223926009
          ],
    tiles='cartodbpositron',
    zoom_start=12,
)
output_df.apply(lambda row: folium.CircleMarker(location=[row["lat"], row["lon"]], popup = row['Property'] + '<p>'+ row['Neighborhood'] +'</p><p>' + row["details"] + '</p?', color = row['color'], radius=6).add_to(map1), axis=1)
map1.save(today + "_map.html")


