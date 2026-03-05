import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy
import seaborn as sns

#laddar in data
data1 = pd.read_csv('video_games_sales.csv')
data2 = pd.read_csv('backloggd_games.csv')

#kollar på kolumnnamnen i båda dataframes för att se att namnen stämmer överens
#Här gick vi manuellt in i backlogged_games.csv och ändrade kolumnnamnet "Name" så att det matchar med "Name" i video_games_sales.csv
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

#kollar shape på dataframe
print(data1.shape)#utifrån .shape funktionern ser vi att det finns 16719 rader och 11 kolumner i dataframen
print(data2.shape)
print(data.shape)#finns 7912 rader och 12 kolumner i den nya dataframen efter merge

#kollar efter saknade värden
print(data.isnull().sum())
#isnull().sum() visar att det finns saknade värden i "Year"(139), "Rating"(651) och "Publisher"(11), vi tar bort dem raderna

#tar bort rader med saknade värden i "Year", "Rating" och "Publisher"
data = data.dropna(subset=['Year', 'Publisher', 'Rating'])
#kontrollerar att de saknade värdena är borttagna
print(data.isnull().sum())
print(data.shape) #kollar hur många rader och kolumner som är kvar efter borttagning
#vi vill ta bort "Rank" kolumnen eftersom den inte är relevant för vår analys
data = data.drop(columns=['Rank'])
print(data.shape) #kollar att "Rank" kolumnen är borttagen

#kollar datatyperna i dataframen
data.info()
#konverterar "Year" kolumnen från float till integer
data["Year"] = data["Year"].astype(int)
#kontrollerar att "Year" kolumnen nu är en integer
data.info()

#kollar på de 5 första raderna i dataframen
print(data.head())

#genomsnittlig global försäljning per genre.
print(data.groupby('Genre')['Global_Sales'].mean().sort_values(ascending=False))

#gör en pivot table för att sammanfatta total försäljning per genre
pivot = pd.pivot_table(data,
                       values='Global_Sales',
                       index='Genre',
                       aggfunc='sum')
print(pivot)

#pieplot för att visa fördelning av försäljning
#summerar försäljning per region
region_sales = data[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()
plt.figure(figsize=(8,8))
plt.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%', startangle=140)
plt.title('Sales Distribution by Region')
plt.axis('equal') #rund cirkel
plt.show()

#scatterplot för att se relationen mellan global sales och user rating
#%matplotlib inline
matplotlib.style.use('ggplot')
plt.scatter(data['Rating'], data['Global_Sales'])
plt.xlabel('User Rating')
plt.ylabel('Global Sales (millions)')
plt.title('Global Sales vs User Rating')
#idxmax hittar indexet på outlier genom att leta efter det största värdet, .loc plockar ut hela raden
outlier = data.loc[data['Global_Sales'].idxmax()]
#Skriver ut datan vi vill ha, så namn, rating och global sales, xytext + textcoords flyttar på texten så den inte hamnar rakt över punkten. 
plt.annotate(outlier['Name'],
             (outlier['Rating'], outlier['Global_Sales']),
             xytext=(5,5),
             textcoords='offset points')
plt.show()

#graf för år med flest släppta spels
data['Year'].value_counts().plot.bar(figsize=(7.5,3))
plt.title('Number of Games Released per Year')
plt.xlabel('Year')
plt.ylabel('Number of Games')
plt.show()

#graf för genre med flest spel
data['Genre'].value_counts().plot.bar(figsize=(7.5,3))
plt.title('Number of Games per Genre')
plt.xlabel('Genre')
plt.ylabel('Number of Games')
plt.show()

#graf för platform med flest spel
data['Platform'].value_counts().plot.bar(figsize=(7.5,3))
plt.title('Number of Games per Platform')
plt.xlabel('Platform')
plt.ylabel('Number of Games')
plt.show()

#graf för publisher med flest spel
data['Publisher'].value_counts().head(10).plot.bar(figsize=(7.5,3))
plt.title('Top 10 Publishers by Number of Games')
plt.xlabel('Publisher')
plt.ylabel('Number of Games')
plt.show()

#graf för publisher som säljer bäst globalt
publisher_sales = data.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=False).head(10)
publisher_sales.plot.bar(figsize=(7.5,3))
plt.title('Top 10 Publishers per Global Sales')
plt.xlabel('Publisher')
plt.ylabel('Total Global Sales (millions)')
plt.show()

#graf för vilken plattform som säljer bäst globalt
platform_sales = data.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False)
platform_sales.plot.bar(figsize=(8,4))
plt.title('Total Global Sales per Platform')
plt.xlabel('Platform')
plt.ylabel('Total Global Sales (millions)')
plt.show()

#graf för att jämföra global sales mellan olika genrer
genre_sales = data.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False)
plt.figure(figsize=(10,6))
genre_sales.plot(kind="barh")
plt.title("Global sales per genre")
plt.xlabel("Global sales (millions)")
plt.ylabel("Genre")
plt.gca().invert_yaxis() #inverterar y-axeln så att den mest sålda genren visas överst
plt.tight_layout() #för att förbättra layouten
plt.show()

#graf för vilken genre som har högst genomsnittlig rating
genre_rating = data.groupby("Genre")["Rating"].mean()
genre_rating.plot(kind="bar")
plt.title("Average Rating per Genre")
plt.ylabel("Average Rating")
plt.xlabel("Genre")
plt.show()

#visualisera med en heatmap för att se korrelationen mellan de olika variablerna
#skapar en variabel för numeriska kolumner
numerical_data = data.select_dtypes(include=['float64', 'int64'])
correlation = numerical_data.corr()
plt.figure(figsize=(7.5,5))
sns.heatmap(correlation,annot=True,linewidths=0.01,vmax=1,square=True,cbar=True)
plt.show()