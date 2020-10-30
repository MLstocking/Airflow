from datetime import datetime
from pytz import timezone
import FinanceDataReader as fdr
from azure.cosmos import CosmosClient
import json


'''
todayPrice 함수
기능: 오늘 하루 동안의 삼성전자 주가 데이터를 수집합니다. 
'''
def todayPrice():
    code = "005930"

    dateformat = '%Y-%m-%d'
    today = datetime.now(timezone('Asia/Seoul'))
    today = today.strftime(dateformat)

    # 데이터 수집 및 전처리
    daily_price = fdr.DataReader(code, today, today)

    if len(daily_price) <= 0:
        raise Exception("No data occurs on weekends.")

    # insert code column
    daily_price.insert(0, 'code', code)
    # drop 'Change' column
    daily_price.drop(columns=['Change'], axis=1, inplace=True)
    # 'Date' index to column
    daily_price.reset_index(inplace=True)
    daily_price.rename(columns={'index': 'Date'}, inplace=True)

    return daily_price



def insert_price(df):
    config = {
        "endpoint": "https://jang.documents.azure.com:443/",
        "primarykey": "xD4e14e4B9hHFCnqwuTqIz9CkKU3APSU5Wcj9KD0tsWaphFBwTYLY9Wr97ks0Q0PBcRfbaqUA9kreBKAMS81nQ=="
    }
    client = CosmosClient(config["endpoint"], config["primarykey"])

    database_name = 'testDatabase'
    database = client.get_database_client(database_name)
    container_name = 'testContainer'
    container = database.get_container_client(container_name)

    # Get the number of items in daily_price container
    continued_items = container.query_items(
        query='SELECT VALUE COUNT(1) FROM daily_price',
        enable_cross_partition_query=True)

    for item in continued_items:
        records_cnt = json.dumps(item, indent=True)

    item_cnt = int(records_cnt)

    # Cosmos DB needs one column named 'id'.
    df['id'] = item_cnt

    # Convert the id column to a string - this is a document database.
    for col in df.columns:
        df[col] = df[col].astype(str)

    # Write rows of a pandas DataFrame as items to the Database Container
    for i in range(0, df.shape[0]):
        # create a dictionary for the selected row
        data_dict = dict(df.iloc[i, :])
        # convert the dictionary to a json object.
        data_dict = json.dumps(data_dict)
        container.upsert_item(json.loads(data_dict))

    print('Records inserted successfully.')


if __name__ == '__main__':
    df = todayPrice()
    insert_price(df)