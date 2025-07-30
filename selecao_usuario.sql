select * from apartamento -- possível acessar a leitura de tabelas, pois há privilégios de leitura

alter table apartamento add column janela bool;
alter table apartamento drop column janela; -- Só é possível fazer tal coisa com o admin_user, pois 
										   -- o usuário "leitor" não é dono da tabela, tampouco tem
										   -- permissão de fazer o que bem entende.
