import time

from etl import ETL

if __name__ == '__main__':
    etl = ETL()

    while True:
        etl.run()
        time.sleep(10)
