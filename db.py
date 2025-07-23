import psycopg2 

def get_connection():
    return psycopg2.connect(
        dbname = 'TrabalhoFinal',
        user = 'postgres',
        password = '1234',
        host = 'localhost'
    )