import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename ="logs/ingestion_db.log",
    level=logging.DEBUG,
    format ="%(asctime)s - %(levelname)s - %(message)s",
    filemode ="a"
)

engine = create_engine('sqlite:///inventory.db')

def ingest_db(df, table_name,engine):
    df.to_sql(
        table_name, 
        con = engine, 
        if_exists = 'replace' , 
        index = False
        )
    
def load_raw_data():
    start = time.time()
    for file in os.listdir("data"):
    # print(file)

        fileName, extension = os.path.splitext(file)

        if extension == ".csv":
            try:
                df = pd.read_csv(os.path.join("data", file))
                logging.info(f'Ingestion {file} in db')
                ingest_db(df, fileName, engine)
                # print(df.shape)
            except:
                for chunks in pd.read_csv(os.path.join("data", file), chunksize=100000):
                    logging.info(f'Ingestion {file} in db')
                    ingest_db(chunks, fileName, engine)
                    # print(chunks.shape)
    end = time.time()
    total_time=(end-start)/60
    logging.info('Ingestion Complete')
    logging.info(f'\nTotal time taken: {total_time} minutes')

if __name__ == "__main__":
    load_raw_data()