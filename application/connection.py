import psycopg2

# conn = psycopg2.connect(
#         host = 'sfs-dev-1-hov.cgktvkinq2gw.us-east-1.rds.amazonaws.com',
#         database = 'postgres',
#         user = 'sfs_db_dev',
#         password = 'sfs123',
#     )
conn = psycopg2.connect(
        host = 'localhost',
        database = 'my_project',
        user = 'postgres',
        password = 'pdnejoh',
    )
cur = conn.cursor()