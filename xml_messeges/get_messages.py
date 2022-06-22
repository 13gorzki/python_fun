import xml.etree.ElementTree as ET
from api import import_data
import pandas as pd
import sqlalchemy as db

'''pobieranie danych z API'''
xml = import_data('Messages')
xml_raw = ET.fromstring(xml)  # parsowanie
print('1. Dane pobrane')

'''strukturyzacja'''
for data in xml_raw.findall('Data'):
    xml_raw.remove(data)
    for messages in data.findall('Messages'):
        for mess in messages.findall('Message'):
            xml_raw.append(mess)
print('2. Ustrukturyzowane')

'''zapisanie do pliku'''
xml_final = ET.ElementTree(xml_raw)
xml_final.write('messages.xml', encoding='utf-8')  # zapisanie do pliku
print('3. Finalny xml zapisany')

'''polaczenie z bd'''
engine = db.create_engine('mssql+pyodbc://loggin:password@ip/database?driver=driver', echo=False)
print('4. Polaczono z baza danych')

'''wrzutka do tabeli'''
df = pd.read_xml('messages.xml', encoding='utf-8')
engine.execute(db.text('''TRUNCATE TABLE table_name''').execution_options(autocommit=True))
print('5. Tabela wyczyszczona')
df.to_sql('table_name', con=engine, if_exists='append', index=False)
print('6. Dane uzupelnione')
