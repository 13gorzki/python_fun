from datetime import date
import sqlalchemy as db
import pandas as pd

''' pobranie tabeli z danymi '''
engine = db.create_engine("mssql+pyodbc://loggin:password@IP/database?driver=driver_ms_sql")
connection = engine.connect()
metadata = db.MetaData()
zapas = db.Table('table_name', metadata, autoload=True, autoload_with=engine)
query = db.select([zapas]).order_by(zapas.columns.Magazyn, zapas.columns.Marka, zapas.columns.Indeks, zapas.columns.IndeksDostawy)
results = connection.execute(query)
result = results.fetchall()

''' wrzutka do dataframe '''
df_raw = pd.DataFrame(result)
df_raw.columns = result[0].keys()
df_raw = df_raw.rename(columns={'Indeks': 'IndeksGl', 'IndeksDostawy': 'IndeksSzcz'})
df_mag = df_raw['Magazyn'].unique().tolist()

''' zmienne '''
folder = '\pliki_excel\BrakujaceEAN'
nrmag = 1


def create_xlsx_for_mag(mag, folders):
    today = date.today().strftime('%Y%m%d')
    df = df_raw[df_raw['Magazyn'] == mag]
    if not df.empty:
        plik = f'{folders}_{mag}_{today}.xlsx'
        writer = pd.ExcelWriter(plik, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format = workbook.add_format()
        format.set_num_format(49)   # 49 = "@"
        worksheet.set_column(8, 8, None, format)
        writer.save()


for mag in df_mag:
    create_xlsx_for_mag(mag, folder)
    print(f'{nrmag}. {mag}')
    nrmag += 1

exec(open('clear_folder.py').read())
