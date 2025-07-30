-- Criando o super usuário admin_user, para fazer isso eu criei como o superuser do postgres.
CREATE ROLE admin_user WITH LOGIN PASSWORD 'abc';
ALTER ROLE admin_user WITH SUPERUSER CREATEDB CREATEROLE REPLICATION BYPASSRLS;

-- Criando o usuário de leitor, similarmente, esse também é feito com o user postgres.

CREATE ROLE leitor WITH LOGIN PASSWORD 'aaa'; -- É possível criar no query tools aqui mesmo, mas no meu caso fizemos isso
											  -- pelo pgAdmin 4.
GRANT USAGE ON SCHEMA public TO leitor;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO leitor;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO leitor;

GRANT USAGE ON SCHEMA public TO outro_leitor;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO outro_leitor;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO outro_leitor;