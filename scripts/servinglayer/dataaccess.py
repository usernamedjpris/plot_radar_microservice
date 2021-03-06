from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import sys
from datetime import datetime
import pandas

client = Elasticsearch(hosts=["192.168.1.53:50000"])


def query_range_date(start_date, end_date, index):

    start_date = datetime.strptime(start_date, '%y/%m/%d-%H:%M')
    end_date = datetime.strptime(end_date, '%y/%m/%d-%H:%M')

    start_ts = datetime.timestamp(start_date)
    end_ts = datetime.timestamp(end_date)

    if end_ts - start_ts < 0:
        raise ValueError("start date must precede end date")

    # print(f'start query on index {index}')

    body = {
        "query": {
            "bool": {
                "must": {"match_all": {}},
                "filter": {
                    "range": {
                        "timestamp": {
                            "gte": start_ts,
                            "lte": end_ts
                        }
                    }
                }
            }
        }
    }

    resp = client.search(index=index,filter_path=['_scroll_id','hits.hits._source'], body=body, scroll="1s", size=1000)
    
    if not "hits" in resp:
        print("no hits for this date range")
        exit(0)

    scroll_id = resp['_scroll_id']
    data = []

    data_aux = [el['_source'] for el in resp['hits']['hits']]
    data += data_aux

    while len(resp['hits']['hits']):

        resp = client.scroll(scroll_id=scroll_id, scroll='1s')
        
        data_aux = [el['_source'] for el in resp['hits']['hits']]
        data += data_aux
        scroll_id = resp['_scroll_id']

    return data

# exp : 20/04/20-00:00 for 20 April 2020
def query_range_date_df(start_date, end_date, index='category48v2'):
    data = query_range_date(start_date, end_date,index)

    df = pandas.DataFrame(data=data)
    #print(data[1:5])
    return df


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("missing argument, please provide : start_date, end_date following year/month/day-hour:minute")
        exit(1)

    index = sys.argv[3] if len(sys.argv) >= 4 else "category48v2"
    resp = query_range_date_df(sys.argv[1], sys.argv[2],index)

    #print(len(resp))
    #print(resp.head(5))
