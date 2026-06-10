import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

matplotlib.use('TkAgg')

# Load Data
data = pd.read_csv("netflix1.csv")

# Basic Info
print(data.head())
print(data.info())
print("Original Shape:", data.shape)

# Remove duplicates
data = data.drop_duplicates()
print("After Removing Duplicates:", data.shape)

# Null Values
print("Null Value Count:\n", data.isnull().sum())


# --- 1. Number of TV Shows and Movies ---
typecount = data['type'].value_counts()
plt.figure(figsize=(12, 4))

# Countplot (Seaborn)
plt.subplot(1, 2, 1)
sns.countplot(data=data, x='type')
plt.title('Movie vs TV Show Count')

# Pie Chart
plt.subplot(1, 2, 2)
plt.pie(typecount, labels=typecount.index, autopct='%.0f%%', colors=['#ff9999','#66b3ff'])
plt.title('Distribution')

plt.tight_layout()

# --- 2. Titles Added to Netflix per Year ---
data['date_added'] = pd.to_datetime(data['date_added'])
data['released_year'] = data['date_added'].dt.year
years_counts = data.groupby(['released_year', 'type']).size().unstack()

ax = years_counts.plot(kind='line', marker='o', figsize=(12, 6))
plt.title('Titles Added to Netflix per Year')
plt.xlabel('Year Added')
plt.ylabel('Number of Titles')
plt.xticks(rotation=45)
plt.yticks(np.arange(0, data['released_year'].max() + 50, 50))  # Adjusted y-ticks
plt.grid(True)
plt.tight_layout()


# --- 3. Age Rating Distribution ---
rating_counts = data.groupby(['rating', 'type']).size().unstack().fillna(0)
ax = rating_counts.sort_values(by='Movie', ascending=False).plot(kind='barh')

# Loop through the bars
for bar in ax.patches:
    width = bar.get_width()-3
    ax.annotate(f'{int(width)}', 
                xy=(width, bar.get_y() + bar.get_height() / 2),
                xytext=(5, 0),  # Offset
                textcoords='offset points',
                ha='left', va='center', fontsize=7)
plt.title('Age Rating Distribution by Type')
plt.xlabel('Number of Titles')
plt.ylabel('Rating')
plt.tight_layout()


# --- 4. Top 10 Countries Posting Content ---
plt.figure(figsize=(10, 5))
top_countries = (
    data['country']
    .dropna()
    .str.split(',', expand=True)
    .stack()
    .str.strip()
    .value_counts()
    .head(10)
)

ax = top_countries.plot(kind="bar", figsize=(10, 5), color='green')

for bar in ax.patches:
    height = bar.get_height()
    ax.annotate(f'{int(height)}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords='offset points',
                ha='center', va='bottom', fontsize=9)
plt.title("Top 10 Countries Posting Content on Netflix")
plt.ylabel("Number of Titles")
plt.xlabel("Country")
plt.xticks(rotation=45)
plt.tight_layout()

#MOVIE DURATION(IN MINS) GRAPH
movies=data[data['type']=='Movie'].copy()
movies= movies[movies['duration'].notnull()]
movies['duration_mins']= movies['duration'].str.extract('(\d+)').astype(int)

print(movies[['title','duration','duration_mins']].head())
plt.figure(figsize=(10, 6))
plt.hist(movies['duration_mins'], bins=30, color='skyblue', edgecolor='black')
plt.title("Distribution of Movie Durations on Netflix")
plt.xlabel("Duration (minutes)")
plt.ylabel("Number of Movies")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

#TV Show Duration(in season) boxplot
tv_shows = data[data['type'] == 'TV Show'].copy()
tv_shows = tv_shows[tv_shows['duration'].notnull()]
tv_shows['season_count'] = tv_shows['duration'].str.extract('(\d+)').astype(int)

season_counts = tv_shows['season_count'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
plt.plot(season_counts.index, season_counts.values, marker='o', color='darkorange', linewidth=2)

plt.title('Number of TV Shows per Season Count on Netflix')
plt.xlabel('Number of Seasons')
plt.ylabel('Number of TV Shows')
plt.xticks(season_counts.index)  # Show all season counts on x-axis
plt.grid(True, linestyle='--', alpha=0.5)

for i, value in enumerate(season_counts.values):
    plt.text(season_counts.index[i], value + 1, str(value), ha='center', fontsize=9)

plt.tight_layout()

#Analyzing which are the top 10 most genre on netflix
genre_data = data['listed_in'].dropna()
all_genres = genre_data.str.split(',', expand=True).stack().str.strip()
genre_counts = all_genres.value_counts()

plt.figure(figsize=(12, 6))
ax=sns.barplot(x=genre_counts.head(10).values, y=genre_counts.head(10).index, palette='rocket')
plt.title('Top 10 Most Popular Genres on Netflix')
plt.xlabel('Number of Titles')
plt.ylabel('Genre')
for i, value in enumerate(genre_counts.head(10).values):
    ax.text(value + 2, i, str(value), va='center', fontsize=9)
plt.tight_layout()

plt.show()