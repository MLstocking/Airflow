import investpy
import json
from azure.cosmos import CosmosClient
from datetime import datetime, timedelta
from pytz import timezone


def get_bond():
    dateformat = '%d/%m/%Y'
    today = datetime.now(timezone('Asia/Seoul'))
    tomorrow = today + timedelta(1)
    today = today.strftime(dateformat)
    tomorrow = tomorrow.strftime(dateformat)

    try:
        df = investpy.get_bond_historical_data(bond='South Korea 10Y', from_date=today, to_date=tomorrow)
        df.reset_index(level=0, inplace=True)
        df = df[['Date', 'Close']]
        return df
    except Exception:
        print("No data occurs on weekends.")
        return []


def insert_bond(df):

    config = {
        "endpoint": "",
        "primarykey": ""
    }

    client = CosmosClient(config["endpoint"], config["primarykey"])

    database_name = 'MLStocking'
    database = client.get_database_client(database_name)
    container_name = 'bond'
    container = database.get_container_client(container_name)

    # Get the number of items in daily_price container
    continued_items = container.query_items(
        query='SELECT VALUE COUNT(1) FROM bond',
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


if __name__ == "__main__":
    bond = get_bond()
    if len(bond) > 0:
        print("Loading...")
        insert_bond(bond)
