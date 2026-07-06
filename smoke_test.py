import boto3
import os
import sys
import pymysql

client = boto3.client('ssm', region_name='ap-northeast-2')

params = {
    os.path.basename(p["Name"]): p["Value"]
    for p in client.get_parameters_by_path(
        Path='/application/banking',
        WithDecryption=True
    )['Parameters']
}

Required = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_PORT"]

missing = [k for k in Required if k not in params]

for k in Required:
    print(f"{k}: {'✅' if k in params else '❌'}")

if missing:
    print(f"Failed : {missing}")
    sys.exit(1)

# DB FIND banking_db and show tables

try:
    connection = pymysql.connect(
        host=params["DB_HOST"],
        user=params["DB_USER"],
        password=params["DB_PASSWORD"],
        database=params["DB_NAME"],
        port=int(params["DB_PORT"]),
        connect_timeout=10
    )

    cur = connection.cursor()
    cur.execute("SHOW TABLES")
    tables = [row[0] for row in cur.fetchall()]
    connection.close()

    print(f"Database : {params['DB_NAME']}")
    print(f"Tables : {tables}")

except pymysql.MySQLError as e:
    print("DB ERROR ❌ :", e)
    sys.exit(1)

print("✅ Smoke Test Done")