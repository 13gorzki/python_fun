'''
2022-04-13 ggorzki:
    Skrypt łączy ze sobą pliki csv i wypluwa obrobione dane do csv
        - pliki tylko ze wskazanego folderu
        - tylko wybrane kolumny (pliki częściowo ustrukturyzowane)
        - do nowego pliku
'''
from datetime import date, timedelta
from os.path import exists
import pandas as pd
import os


def listing_directory(directory, when):
    last_3_days = date.today() - timedelta(days=when)
    file_name_import = []
    with os.scandir(directory) as files:
        for file in files:
            p_name = file.name
            atime = date.fromtimestamp(file.stat().st_atime)
            mtime = date.fromtimestamp(file.stat().st_mtime)
            if (atime >= last_3_days or mtime >= last_3_days ) and file.is_file() and p_name.endswith('.csv'):
                file_name_import.append(p_name)
    return file_name_import


def reorganization_file(file_from_directory):
    df_to_csv = pd.DataFrame()
    n = 1
    print('Imported:')
    for file in file_from_directory:
        data = pd.read_csv(directory + file, delimiter=';', encoding='cp1252', dtype=object)
        data = data.dropna(axis=0, how='all')  # usuniecie pustych wierszy
        head_raw = data.columns.values
        head = ['Order_ConfirmedAmount' if 'Order_ConfirmedAmount' in h else h for h in
                head_raw]  # usuniecie dziwnego znaku ktorego nierozpoznaje utf-8
        data = data.rename(columns={head_raw[0]: head[0]})
        data.insert(0, 'NazwaPliku', file)  # dodanie nazwy importowanego pliku
        data = data[header]
        df_to_csv = pd.concat([df_to_csv, data], ignore_index=True)
        print(f'{n}. {file};')
        n += 1
    return df_to_csv


directory = '/Desktop/file_to_import/'    
new_file = 'dane_import.csv'
header = ['NazwaPliku', 'Wartosc', 'Ilosc', 'NrNadawcy',
              'NazwaProd', 'KodProd', 'Sezon', 'DataDost', 'NrZam',
              'NrOdbiorcy', 'Detal', 'Rozmiar', 'Hurt', 'EAN', 'Kupiec',
              'Marka', 'Rabat', 'Opis_zamowienia', 'Grupa', 'Przeznaczenie', 'Plec',
              'CenaZakJedn', 'VATzak', 'VATspr', 'TermPay']


files = listing_directory(directory, 3)

if files:
    if exists(new_file):
        os.remove(new_file)
    df = reorganization_file(files)
    df.to_csv(new_file, sep=';', columns=header, index=False, mode='a', encoding='utf-8')    # export danych do csv
    print('Success, everything was successfully imported and exported.')
else:
    print('There are no files to import and export')
