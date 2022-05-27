from datetime import date
import sqlalchemy as db
import pandas as pd

# pobranie tabeli z danymi
engine = db.create_engine("mssql+pyodbc://login:password@sever_ip/database_name?driver=ODBC+Driver+17+for+SQL+Server")
connection = engine.connect()
metadata = db.MetaData()
data = db.Table('Table_name', metadata, autoload=True, autoload_with=engine)

query = db.select([data]).order_by(data.columns.Magazyn, data.columns.Marka, data.columns.Indeks, data.columns.IndeksDostawy)
results = connection.execute(query)
result = results.fetchall()

# wrzutka do dataframe
df_raw = pd.DataFrame(result)
df_raw.columns = result[0].keys()
df_raw = df_raw.rename(columns={'Indeks': 'IndeksGl', 'IndeksDostawy': 'IndeksSzcz'})

# wyciagniecie magazynow
df_mag = df_raw['Magazyn'].unique().tolist()

# zmienne
folder = 'C:\(...)\pliki_excel\file_without_EAN'
today = date.today().strftime('%Y%m%d')
nrmag = 1

# utworzenie plikow excel
for mag in df_mag:
    df = df_raw[df_raw['Magazyn'] == mag]
    if not df.empty:
        plik = f'{folder}_{mag}_{today}.xlsx'
        writer = pd.ExcelWriter(plik, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format = workbook.add_format()
        format.set_num_format(49)   # 49 = "@" format text
        worksheet.set_column(8, 8, None, format)
        writer.save()
        print(f'{nrmag}. {mag}')
        nrmag += 1
