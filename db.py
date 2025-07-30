import psycopg2 

def get_connection():
    return psycopg2.connect(
        dbname = 'Trabalho_Final',
        user = 'postgres',
        password = 'Admiral01',
        host = 'localhost'
    )