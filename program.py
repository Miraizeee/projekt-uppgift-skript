import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy
import seaborn as sns

#laddar in data
data1 = pd.read_csv('video_games_sales.csv')
data2 = pd.read_csv('backloggd_games.csv')
#data.info()

#kollar på kolumnnamnen i båda dataframes för att se att namnen stämmer överens
print(data1.columns)
print(data2.columns)

#för matchning tas mellanslag och stora bokstäver bort
data1['Name'] = data1['Name'].str.strip().str.lower()
data2['Name'] = data2['Name'].str.strip().str.lower()

#tar bort dubbletter i data2 baserat på "Name" kolumnen
data2_unique = data2.drop_duplicates(subset=['Name'])
#lägger till user rating i data1 genom att använda merge funktionen och anger "Name" som nyckel
data = pd.merge(data1, data2_unique[['Name', 'Rating']], on='Name',how='inner') # inner= bara spel som finns i båda filerna
print(data)

"""
#kollar shape på dataframe
print(data1.shape)#utifrån .shape funktionern ser vi att det finns 16719 rader och 11 kolumner i dataframen
print(data2.shape)
print(data.shape)#finns 7912 rader och 12 kolumner i den nya dataframen efter merge
"""

#kollar på de 5 första raderna i dataframen
print(data.head())

#kollar efter saknade värden
print(data.isnull().sum())
#isnull().sum() visar att det finns saknade värden i "Year" och "Publisher", vi tar bort dem raderna

data = data.dropna(subset=['Year', 'Publisher', 'Rating'])
#kontrollerar att de saknade värdena är borttagna
print(data.isnull().sum())
print(data.shape) #kollar hur många rader och kolumner som är kvar efter borttagning
#vi vill ta bort "Rank" kolumnen eftersom den inte är relevant för vår analys
data = data.drop(columns=['Rank'])
print(data.shape) #kollar att "Rank" kolumnen är borttagen

#pieplot för att visa fördelning av försäljning
#summerar försäljning per region
region_sales = data[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()
plt.figure(figsize=(8,8))
plt.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%', startangle=140)
plt.title('Sales Distribution by Region')
plt.axis('equal') #rund cirkel
plt.show()
""""
#scatterplot för att se relationen mellan global sales och user rating
#%matplotlib inline
matplotlib.style.use('ggplot')
plt.scatter(data['Rating'], data['Global_Sales'])
plt.xlabel('User Rating')
plt.ylabel('Global Sales (millions)')
plt.title('Global Sales vs User Rating')
plt.show()


#skapar en graf som visar år med flest spel släppta, mest populära genrer, plattformar och utgivare
data['Year'].value_counts().plot.bar(figsize=(7.5,3))
plt.show()
data['Genre'].value_counts().plot.bar(figsize=(7.5,3))
plt.show()
data['Platform'].value_counts().plot.bar(figsize=(7.5,3))
plt.show()
data['Publisher'].value_counts().head(10).plot.bar(figsize=(7.5,3))
plt.show()

#graf för att jämföra global sales mellan olika genrer
genre_sales = data.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)
plt.figure(figsize=(10,6))
genre_sales.plot(kind="barh")

plt.title("Global sales per genre")
plt.xlabel("Global sales (millions)")
plt.ylabel("Genre")
plt.gca().invert_yaxis() 
plt.tight_layout()
plt.show()


#visualisera med en heatmap för att se korrelationen mellan de olika variablerna
#skapar en variabel för numeriska kolumner
numerical_data = data.select_dtypes(include=['float64', 'int64'])
correlation = numerical_data.corr()
plt.figure(figsize=(7.5,5))
sns.heatmap(correlation,annot=True,linewidths=0.01,vmax=1,square=True,cbar=True)
plt.show()
"""