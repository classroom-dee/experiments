## PostgreSQL(13) Dissection Experiment
### 1. Setup
- Docker compose setup for psql, exporter, prometheus, grafana
- 'Data', 'grafana-data' folder for volumes
- Environs defined in a .env file (see docker compose)
- prometheus.yml (NOT yaml or it won't be recognized)
### 2. Dataset(s)
- [NYC Taxi Trip Duration](https://www.kaggle.com/competitions/nyc-taxi-trip-duration/data)
- Only the train.csv was used.
- bla
### 3. Copy to DB
```sql
CREATE TABLE nyc_taxi (
    id TEXT PRIMARY KEY,
    vendor_id INTEGER,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    passenger_count INTEGER,
    pickup_longitude FLOAT,
    pickup_latitude FLOAT,
    dropoff_longitude FLOAT,
    dropoff_latitude FLOAT,
    store_and_fwd_flag TEXT,
    trip_duration INTEGER
);
```
-> 1458644 rows

### DQL
- Stress test on a non-indexible query
- But is this meaningful?? Who would use such a query and in what use cases?
```sql
select * 
from nyc_taxi 
where pickup_datetime 
not in (
    select pickup_datetime
    from nyc_taxi 
);
```
![alt text](image.png)
35billion??

### Reads
- [On buffer shared hit and read](https://pganalyze.com/blog/5mins-explain-analyze-buffers-nested-loops)
- Buffer hit diff bw nested loop and others
