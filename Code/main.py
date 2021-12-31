import pandas as pd
import pathlib
# load the csv file into a pandas data frame
df_mobility = pd.read_csv('../Data/Ladesaeulenregister_CSV.csv', encoding='latin_1', sep=';', skiprows=5)
# CP850

#print(df_mobility)

# print('Hello, world!')

# translate columns into english 
old_names = df_mobility.columns.tolist()

new_names = ['operator', 'address', 'house_number', 'placeholder1', 'postcode', 'city', 'federal_state', 'metropolitan_area', 
                'longitude_[dg]', 'latitude_[dg]', 'commissioning_date',
                'power_connection_[kw]', 'type_of_charger', 'number_of_charging_points','type_of_plug_1', 'p1_[kw]', 
             'public_key1', 'type_of_plug_2', 'p2_[kw]', 'public_key2', 'type_of_plug_3', 'p3_[kw]', 'public_key3',
             'type_of_plug_4', 'p4_[kw]', 'public_key4']

df_mobility.rename(columns=dict(zip(old_names, new_names)), inplace=True)

# unique elements of the column type_of_charger
df_mobility.type_of_charger.unique()
# array(['Schnellladeeinrichtung', 'Normalladeeinrichtung'], dtype=object)

# modify entries of the column type_of_charger
df_mobility.type_of_charger.replace({'Schnellladeeinrichtung': 'fast', 'Normalladeeinrichtung': 'normal'}, inplace=True)

# basic summary of the data frame
# df_mobility.info()

# replace null values by 0
columns_na = ['type_of_plug_2', 'p2_[kw]', 'type_of_plug_3', 'p3_[kw]', 'type_of_plug_4', 'p4_[kw]']

for column in columns_na:
    df_mobility[column] = df_mobility[column].fillna(value='0')

# drop public key columns
df_mobility.drop(columns=['public_key1', 'public_key2', 'public_key3', 'public_key4'], inplace=True)

# check if there are null values
df_mobility.isnull().sum().sum()
# 0

# basic summary of the data frame
# df_mobility.info()

# convert the data type of these columns to float
columns_modify =  ['longitude_[dg]', 'latitude_[dg]', 'power_connection_[kw]', 'p1_[kw]', 'p2_[kw]', 'p3_[kw]', 'p4_[kw]']

for column in columns_modify: 
    df_mobility[column] = df_mobility[column].str.replace(',','.').astype('float')

# convert the column commissioning_date to datetime
df_mobility['commissioning_date'] = pd.to_datetime(df_mobility['commissioning_date'], format='%d.%m.%Y')

# check that inappropriate data types and null values were correctly modified
# df_mobility.info()

# there are city names with leading or trailing spaces
df_mobility.city[df_mobility.city.str.startswith(' ') | df_mobility.city.str.endswith(' ')].unique()

# names of columns of type object
columns_object = df_mobility.select_dtypes(include='object').columns

# remove leading and trailing spaces of columns of type object using the string method strip
for column in columns_object:
    df_mobility[column] = df_mobility[column].str.strip()

# check that leading and trailing spaces of the column city were correctly removed
(df_mobility.city.str.startswith(' ') | df_mobility.city.str.endswith(' ')).any()
# False

# series containing city names
cities = df_mobility.city

# discover wrong city names using the contains method
cities[cities.str.contains('Frankfurt')].unique()
# array(['Frankfurt (Oder)', 'Frankfurt/Oder', 'Frankfurt',
#        'Frankfurt am Main', 'Frankfurt-Niederrad'], dtype=object)

cities[cities.str.contains('Stuttgart')].unique()
# array(['Stuttgart', 'Stuttgart-Obertürkheim', 'Stuttgart-Mühlhausen',
#        'Stuttgart-Möhringen'], dtype=object)

cities[cities.str.contains('München')].unique()
# array(['Stuttgart', 'Stuttgart-Obertürkheim', 'Stuttgart-Mühlhausen',
#        'Stuttgart-Möhringen'], dtype=object)


# cities_modification2={'M¸nchen': 'München'}
# df_mobility.city.replace(cities_modification2, inplace=True)

# map wrong names to correct denominations
cities_modification = {'Hamburg-Wandsbeck': 'Hamburg', 'Hamburg-Duvenstedt': 'Hamburg', 'Berlin-Köpenick': 'Berlin',
                       'Berlin-Friedrichsfelde': 'Berlin', 'Berlin-Reinickendorf': 'Berlin', 'Köln-Niehl': 'Köln',
                       'Köln-Merheim': 'Köln', 'Frankfurt': 'Frankfurt am Main', 'Frankfurt-Niederrad': 'Frankfurt am Main',
                       'Stuttgart-Obertürkheim': 'Stuttgart', 'Stuttgart-Mühlhausen': 'Stuttgart', 'Stuttgart-Möhringen': 'Stuttgart',
                       'Leipzig-Gohlis': 'Leipzig', 'Essen-Kettwig': 'Essen', 'Bremen-Vahr': 'Bremen', 'Dresden Gabitz': 'Dresden',
                       'Dresden Striesen': 'Dresden', 'Regensburg-Schwabelweis': 'Regensburg', 'Wuppertal Vohwinkel': 'Wuppertal', 
                       'Garching b. München': 'München', 'München - Neufriedenheim': 'München', 'München Flughafen': 'München', 
                       'München Nord': 'München', 'München Sendling': 'München', 'München-Flughafen': 'München', 
                       'München-Freiham': 'München', 'Puchheim b. München': 'München'}
# replace wrong values
df_mobility.city.replace(cities_modification, inplace=True)

# check that the modification was carried out correctly
cities[cities.str.contains('Stuttgart')].unique()
# array(['Stuttgart'], dtype=object)

# number of duplicated rows
df_mobility.duplicated().sum()
# 1001

import matplotlib.pyplot as plt

# matplotlib inline
plt.style.use('seaborn')

# number of charging station per federal state
df_mobility.federal_state.value_counts().plot(kind='bar', color='green', figsize=(8,6))

# modify ticks size
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# title and labels
plt.title('Number of charging stations by federal state', fontsize=20)
plt.xlabel('State', fontsize=16)
plt.ylabel('Number', fontsize=16)

# plt.show()
plt.savefig('../Exploratory_Analysis_Graphs/EVperFederalState.png', bbox_inches='tight')
plt.cla()

# top 10 German cities with the most EV charging stations
df_mobility.city.value_counts().head(10).plot(kind='bar', color='blue', figsize=(8,6))

# modify ticks size
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# title and labels
plt.title('Top 10 German cities with the most EV charging stations', fontsize=20)
plt.xlabel('City', fontsize=16)
plt.ylabel('Number', fontsize=16)

# plt.show()
plt.savefig('../Exploratory_Analysis_Graphs/Top10GermanCity.png', bbox_inches='tight')
plt.cla()

# number of charging stations located in Munich, Hamburg, or Berlin
# top_three = df_mobility.city.isin(['Berlin', 'München', 'Hamburg']).sum()
num_Munich=df_mobility.city.isin(['München']).sum()
num_Berlin=df_mobility.city.isin(['Berlin']).sum()
num_Hamburg=df_mobility.city.isin(['Hamburg']).sum()

top_three=num_Munich+num_Berlin+num_Hamburg
# number of charging stations in Germany
total = df_mobility.shape[0]

# percentage of charging stations located in Munich, Hamburg, or Berlin
perc=top_three/total*100
print('Num of Munich:', num_Munich)
print('Num of Berlin:', num_Berlin)
print('Num of Hamburg:', num_Hamburg)
print('Sum of Berlin+München+Hamburg', top_three, 'wrt total Germany', total)
print('Percentage of Berlin, München, Hamburg', perc)
# 9.11

# number of charging points of stations in Germany - pie chart
df_mobility['number_of_charging_points'].value_counts().plot(kind='pie', figsize=(7,7), autopct='%1.1f%%', fontsize=16)

# labels and title
plt.title('Number of charging points of stations in Germany', fontsize=20)
plt.ylabel('')

# plt.show()
plt.savefig('../Exploratory_Analysis_Graphs/ChargingPointNumber.png', bbox_inches='tight')
plt.cla()

# top 10 German cities with the most EV charging points
df_mobility.groupby('city').sum().number_of_charging_points.sort_values(ascending=False).head(10).plot(kind='bar', color='maroon', figsize=(8,6))

# modify ticks size
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# title and labels
plt.title('Top 10 German cities with the most EV charging points',fontsize=20)
plt.xlabel('City',fontsize=16)
plt.ylabel('Number',fontsize=16)

plt.show()
plt.savefig('../Exploratory_Analysis_Graphs/GermanCityPerChargingPoints.png', bbox_inches='tight')
plt.cla()

# number of new charging stations installed per year
df_mobility['commissioning_date'].dt.year.value_counts().sort_index().plot(kind='bar', color='darkblue')

# modify ticks size
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# title and labels
plt.title('Number of new charging stations installed per year',fontsize=20)
plt.xlabel('Year',fontsize=16)
plt.ylabel('Number',fontsize=16)

# plt.show()
plt.savefig('../Exploratory_Analysis_Graphs/ImprovementEVChargingStationPerYear.png', bbox_inches='tight')
plt.cla()

# the last date recorded was May 5th 2020
print('Last date Update', df_mobility['commissioning_date'].max())
# Timestamp('2021-11-01 00:00:00')

p1, p2, p3, p4 = df_mobility['p1_[kw]'], df_mobility['p2_[kw]'], df_mobility['p3_[kw]'], df_mobility['p4_[kw]']

# serie that contains the power of all charging points in Germany
charging_points = pd.concat([p1, p2, p3, p4])

# remove entries equal to 0 
charging_points = charging_points[charging_points != 0]

# 10 most common power
most_common_power = charging_points.value_counts().head(10)

# print(most_common_power)

import numpy as np

# number of unique power outputs in Germany
charging_points.nunique()
# print('number of unique points', charging_points.nunique())
# 86

# unique power outputs sorted in ascending order 
np.sort(charging_points.unique())

#--------------------------------------------------------------------------------------------------------------------
# number of charging points with a power output different from 22, 11, 50, 43, 3.7, 350, 150, 42, 20, 53 (10 most common power outputs)
num_charging_points = charging_points.count()
other_power = num_charging_points - most_common_power.sum()

# include other in the most common power output serie
most_common_power.at['other'] = other_power

# define colors of the pie plot
colors = ['darkviolet', 'dodgerblue', 'yellow', 'deeppink', 'orange', 'skyblue', 'salmon', 'green', 'red', 'darkblue', 'springgreen']

# pie plot showing power output of charging points in Germany
most_common_power.plot(kind='pie', figsize=(8, 8), labels=None, colors=colors, fontsize=16)

# legend  - percentage of charging points 
labels = ['{} kW - {:.2%}'.format(index, most_common_power.loc[index]/num_charging_points) for index in most_common_power.index]
plt.legend(labels, loc='best', bbox_to_anchor=(-0.1, 1.), fontsize=18)

# labels and title
plt.title('Power output of charging points in Germany', fontsize=20)
plt.ylabel('')
# plt.show()
plt.savefig('../Exploratory_Analysis_Graphs/PowerOutputPiePercentage.png', bbox_inches='tight')
plt.cla()
#--------------------------------------------------------------------------------------------------------------------

# number of charging points of 300 kW in operation
(charging_points == 300.0).sum()
#print('Number of charging point 300kW:', (charging_points == 300.0).sum())
# 6 on May 2020
# 582 on Nov 2021

# number of charging points of 320 kW in operation 
(charging_points == 320.0).sum()
#print('Number of charging point 300kW:', (charging_points == 320.0).sum())
# 10 on May 2020
# 65 on Nov 2021

# number of charging points of 350 kW in operation 
(charging_points == 350.0).sum()
#print('Number of charging point 300kW:', (charging_points == 350.0).sum())
# 328 on May 2020
# 462 on Nov 2021

# charging stations with at least one ultra-rapid charging point (>300kW)
ultra_fast_stations = df_mobility[(df_mobility['p1_[kw]']>=300.0) | (df_mobility['p2_[kw]']>=300.0) | (df_mobility['p3_[kw]']>=300.0) | (df_mobility['p4_[kw]']>=300.0)]

# number of charging stations with at least one ultra-rapid charging point
# print('Number of ultra fast stations', len(ultra_fast_stations))
# 341 on May 2020
# 821 on November 2021

# number of charging station with ultra-rapid charger
ultra_fast_stations.federal_state.value_counts().plot(kind='bar', color='springgreen', figsize=(8,6))

# print(ultra_fast_stations)

# modify ticks size
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# title and labels
plt.title('Number of stations with ultra-rapid chargers', fontsize=20)
plt.xlabel('State', fontsize=16)
plt.ylabel('Number', fontsize=16)

plt.savefig('../Exploratory_Analysis_Graphs/UltraRapidChargersPerLand.png', bbox_inches='tight')
plt.cla()
#--------------------------------------------------------------------------------------------------------------------

# number of new charging stations with ultra-rapid chargers
ultra_fast_stations['commissioning_date'].dt.year.value_counts().sort_index().plot(kind='bar', color='royalblue')

# modify ticks size
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# title and labels
plt.title('Number of new charging stations with ultra-rapid chargers', fontsize=20)
plt.xlabel('Year', fontsize=16)
plt.ylabel('Number', fontsize=16)

# plt.show()
################## ACHTUNG
#--------------------------------------------------------------------------------------------------------------------

# first electric vehicle charging station in Germany
print('First EV charging station:', df_mobility['commissioning_date'].min())
# Timestamp('1999-12-31 00:00:00')

# first charging station with an ultra-rapid charging point (>300kW) in Germany.
print('First ultra-rapid charging station:', ultra_fast_stations['commissioning_date'].min())
# Timestamp('2012-06-16 00:00:00')

#--------------------------------------------------------------------------------------------------------------------

# the most populated cities in Germany
biggest_cities = ['Berlin', 'Hamburg', 'München', 'Köln', 'Frankfurt am Main', 'Stuttgart', 'Düsseldorf', 'Dortmund', 'Essen', 'Leipzig']

# group by date and city
date_city_group_by = df_mobility.groupby([df_mobility['commissioning_date'].dt.year, 'city']).count()

# select a column and move the innermost level of the index to the columns
date_cities = date_city_group_by.operator.unstack()

# select the most populated cities in germany
date_cities_10 = date_cities[biggest_cities]

date_cities_10