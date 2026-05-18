import pandas as pd

print("--- Rozpoczynam czyszczenie danych dla Rio de Janeiro ---")

df = pd.read_csv('/Users/marcingorecki/Desktop/Python/Big Data/listings.csv', encoding='utf-8', low_memory=False)
print(f"Początkowa liczba rekordów: {df.shape[0]}")

kolumny_do_zostawienia = [
    'id', 'name', 'host_id', 'host_name', 'host_is_superhost', 
    'neighbourhood_cleansed', 'room_type', 'price', 
    'minimum_nights', 'number_of_reviews', 'review_scores_rating', 'review_scores_location'
]
df = df[kolumny_do_zostawienia]

df['price'] = df['price'].astype(str).str.replace('R$', '', regex=False)
df['price'] = df['price'].str.replace('$', '', regex=False)
df['price'] = df['price'].str.replace(',', '', regex=False).astype(float)

df = df[(df['price'] > 0) & (df['price'] <= 15000)]

df['host_is_superhost'] = df['host_is_superhost'].fillna('f')

mediana_ocen = df['review_scores_rating'].median()
df['review_scores_rating'] = df['review_scores_rating'].fillna(mediana_ocen)

mediana_lokalizacji = df['review_scores_location'].median()
df['review_scores_location'] = df['review_scores_location'].fillna(mediana_lokalizacji)

df['host_name'] = df['host_name'].fillna('Unknown')

nowe_nazwy = {
    'id': 'ID_oferty',
    'name': 'Nazwa_oferty',
    'host_id': 'ID_hosta',
    'host_name': 'Nazwa_hosta',
    'host_is_superhost': 'Czy_Superhost',
    'neighbourhood_cleansed': 'Dzielnica',
    'room_type': 'Typ_pokoju',
    'price': 'Cena_R$',
    'minimum_nights': 'Minimalna_liczba_nocy',
    'number_of_reviews': 'Liczba_recenzji',
    'review_scores_rating': 'Ocena_ogolna',
    'review_scores_location': 'Ocena_lokalizacji'
}
df = df.rename(columns=nowe_nazwy)

df.to_csv('/Users/marcingorecki/Desktop/Python/Big Data/rio_airbnb_wyczyszczone.csv', index=False, encoding='utf-8')

print(f"Koncowa liczba rekordów po czyszczeniu: {df.shape[0]}")
print("Plik 'rio_airbnb_wyczyszczone.csv' jest gotowy do wrzucenia do MS Access!")