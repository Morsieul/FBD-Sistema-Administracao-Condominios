CREATE SEQUENCE ID_Telefone_seq START WITH 1;

CREATE TABLE Telefone (
  ID_Telefone INT PRIMARY KEY DEFAULT nextval('ID_Telefone_seq'),
  DDD CHAR(2) NOT NULL,
  Telefone CHAR(9) NOT NULL
);

CREATE TABLE Condomino(
	CPF_Condomino VARCHAR(11) NOT NULL,
	Nome_Condomino VARCHAR(200) NOT NULL,
	Data_nasc DATE NOT NULL,
	ID_Telefone INT NOT NULL,

	PRIMARY KEY(CPF_Condomino),
	FOREIGN KEY(ID_Telefone) REFERENCES Telefone(ID_Telefone)
);

CREATE SEQUENCE ID_Dependente_seq;
CREATE TABLE Dependente(
	ID_Dependente INT DEFAULT nextval('ID_Dependente_seq'),
	CPF_Dependente VARCHAR(11) NOT NULL,
	CPF_Condomino VARCHAR(11) NOT NULL,
	Nome_Dependente VARCHAR(200) NOT NULL,

	PRIMARY KEY(ID_Dependente),
	FOREIGN KEY(CPF_Condomino) REFERENCES Condomino(CPF_Condomino),
	UNIQUE(CPF_Dependente)
);

CREATE SEQUENCE ID_Area_seq;
CREATE TABLE Area_Comum(
	ID_Area INT DEFAULT nextval('ID_Area_seq'),
	Nome_Local VARCHAR(30) NOT NULL,
	CPF_Condomino VARCHAR(11), -- Pode ser nulo, caso a área exista mesmo sem reserva
	Data_Reserva TIMESTAMP, -- Pode ser nulo, caso a área exista mesmo sem reserva
	
	PRIMARY KEY(ID_area),
	FOREIGN KEY(CPF_Condomino) REFERENCES Condomino(CPF_Condomino)
);

ALTER TABLE Area_Comum DROP CPF_Condomino;
ALTER TABLE Area_Comum DROP Data_Reserva;

CREATE SEQUENCE ID_Reserva_seq;
CREATE TABLE Reserva_Area(
	ID_Reserva INT DEFAULT nextval('ID_Reserva_seq'),
	ID_Area INT NOT NULL,
	CPF_Condomino VARCHAR(11) NOT NULL,
	Data_Reserva TIMESTAMP NOT NULL, 
	
	PRIMARY KEY(ID_Reserva),
	FOREIGN KEY(ID_Area) REFERENCES Area_Comum(ID_Area),
	FOREIGN KEY(CPF_Condomino) REFERENCES Condomino(CPF_Condomino)
);


CREATE TABLE Apartamento(
	Numero_Apartamento INT NOT NULL,
	CPF_Condomino VARCHAR(11), -- Pode ser nulo, caso não esteja alugado
	Descricao_Comodo VARCHAR(200) NOT NULL, -- quantidade de quartos, banheiros, etc
	qtd_quartos INT NOT NULL,
	Valor FLOAT NOT NULL,
	
	PRIMARY KEY(Numero_Apartamento),
	FOREIGN KEY(CPF_Condomino) REFERENCES Condomino(CPF_Condomino)
);

CREATE SEQUENCE ID_Aluguel_seq;
CREATE TABLE Aluguel(
	ID_Aluguel INT DEFAULT nextval('ID_Aluguel_seq'),
	Numero_Apartamento INT NOT NULL,
	CPF_Condomino VARCHAR(11), -- Pode ser nulo, caso não esteja alugado
	Valor NUMERIC NOT NULL,
	Data_Entrada TIMESTAMP, -- Pode ser nulo, caso não esteja alugado
	Data_Saida TIMESTAMP, -- Pode ser nulo, caso não esteja alugado

	PRIMARY KEY(ID_Aluguel),
	FOREIGN KEY(Numero_Apartamento) REFERENCES Apartamento(Numero_Apartamento),
	FOREIGN KEY(CPF_Condomino) REFERENCES Condomino(CPF_Condomino)
);

CREATE SEQUENCE ID_Pagamento_seq;
CREATE TABLE Pagamento(
	ID_Pagamento INT DEFAULT nextval('ID_Pagamento_seq'),
	CPF_Condomino VARCHAR(11) NOT NULL,
	Numero_Apartamento INT NOT NULL,

	PRIMARY KEY(ID_Pagamento),
	FOREIGN KEY(CPF_Condomino) REFERENCES Condomino(CPF_Condomino),
	FOREIGN KEY(Numero_Apartamento) REFERENCES Apartamento(Numero_Apartamento)
);

CREATE SEQUENCE ID_recibo_seq;
CREATE TABLE RECIBO(
	ID_Recibo INT DEFAULT nextval('ID_recibo_seq'),
	CPF_Condomino VARCHAR(11) NOT NULL,
	ID_Pagamento INT NOT NULL,

	PRIMARY KEY(ID_Recibo),
	FOREIGN KEY(CPF_Condomino) REFERENCES Condomino(CPF_Condomino),
	FOREIGN KEY(ID_Pagamento) REFERENCES Pagamento(ID_Pagamento)
)

ALTER TABLE Pagamento
add Data_Pagamento TIMESTAMP NOT NULL;

ALTER TABLE Apartamento 
ALTER COLUMN qtd_quartos DROP NOT NULL, ALTER COLUMN Valor DROP NOT NULL;

-- # # # # Popular o banco de dados: # # # #
-- telefones
INSERT INTO Telefone (ddd, telefone) values
	('11', '912345678'),
	('21', '987654321'),
	('31', '998877665'),
	('41', '934567890'),
	('51', '976543210'),
	('61', '923456789'),
	('71', '945612378'),
	('81', '956789012'),
	('91', '967890123'),
	('27', '978901234'),
	('21', '998765432'),
	('31', '987654331'),
	('41', '996543210'),
	('51', '995432198')
;

-- condôminos
INSERT INTO Condomino (cpf_condomino, nome_condomino, data_nasc, id_telefone) VALUES
  ('12345678900', 'Ana Souza', '2000-03-15', 1),
  ('98765432111', 'Bruno Lima', '1998-07-22', 2),
  ('32198765422', 'Carla Mendes', '2001-01-10', 3),
  ('45612378933', 'Diego Rocha', '1999-12-05', 4),
  ('78932145644', 'Elaine Castro', '2002-06-30', 5),
  ('23456789055', 'Fábio Almeida', '1997-09-18', 6),
  ('89012345666', 'Gabriela Nunes', '2000-11-03', 7),
  ('67834591277', 'Henrique Dias', '1996-05-25', 8),
  ('54321987688', 'Isabela Freitas', '2003-02-14', 9),
  ('10987654399', 'João Pereira', '1995-08-09', 10),
  ('65432198700', 'Marcela Tavares', '2004-04-12', 11),
  ('78965412388', 'Rodrigo Martins', '1999-11-23', 12),
  ('32109876544', 'Vanessa Oliveira', '2001-07-05', 13),
  ('98732165411', 'Eduardo Ramos', '1997-02-16', 14);

-- dependentes dos condominos
INSERT INTO Dependente(cpf_condomino, cpf_dependente, nome_dependente) values
	('12345678900', '55544433321', 'Lucas Souza'),
	('12345678900', '44433322219', 'Marina Souza'),
	('98765432111', '33322211118', 'Felipe Lima'),
	('32198765422', '22211100017', 'Thiago Mendes'),
	('32198765422', '11100099916', 'Lívia Mendes'),
	('45612378933', '00099988815', 'Rafael Rocha'),
	('78932145644', '99988877714', 'Clara Castro'),
	('23456789055', '88877766613', 'Pedro Almeida'),
	('23456789055', '77766655512', 'Sofia Almeida'),
	('89012345666', '66655544411', 'Mateus Nunes'),
	('89012345666', '55544433310', 'Laura Nunes'),
	('67834591277', '44433322209', 'Bruno Dias'),
	('54321987688', '33322211108', 'Camila Freitas'),
	('54321987688', '22211100007', 'Daniel Freitas'),
	('54321987688', '11100099906', 'Beatriz Freitas'),
	('10987654399', '00099988805', 'Gustavo Pereira'),
	('10987654399', '99988877704', 'Helena Pereira'),
	('10987654399', '88877766603', 'Vinícius Pereira'),
	('45612378933', '77766655502', 'Juliana Rocha'),
	('78932145644', '66655544401', 'André Castro')
;

-- áreas comuns
INSERT INTO Area_Comum(nome_local) values
	('Salão de festas'),
	('Churrasqueira'),
	('Quadra de Futsal'),
	('Quadra de Vôlei'),
	('Piscina'),
	('Academia'),
	('Sala de jogos'),
	('Cinema'),
	('Playground'),
	('Rooftop')
;

-- apartamentos
INSERT INTO Apartamento(numero_apartamento, descricao_comodo) values
	(101, '2 quartos, jardim privativo, 59m².'),
	(102, 'Studio moderno, mobiliado, 36m².'),
	(103, '1 quarto, cozinha americana, ideal para estudantes, 38m².'),
	(104, '1 quarto, sala integrada, ideal para solteiros ou casais, 42m².'),
	(201, 'Studio com varanda e vista livre, ideal para home office, 35m².'),
	(202, '1 suíte, varanda com fechamento em vidro, mobiliado, 40m².'),
	(203, '1 quarto, varanda privativa, cozinha planejada, 48m².'),
	(204, 'Loft moderno com pé-direito duplo e mezanino, 50m².'),
	(301, '2 quartos, 1 banheiro, área de serviço separada, 55m².'),
	(302, '2 quartos, 1 banheiro, piso em porcelanato, 58m².'),
	(303, '2 quartos, 1 suíte, varanda integrada à sala, piso laminado, 64m².'),
	(304, '3 quartos, 1 suíte, cozinha americana, 78m².'),
	(401, '2 quartos, 1 suíte, varanda com vista para o jardim, 65m².'),
	(402, '2 quartos, andar alto, ventilado, com armários planejados, 60m².'),
	(403, '3 quartos, 1 suíte, cozinha com armários planejados, 82m².'),
	(501, '3 quartos, varanda gourmet com churrasqueira, 85m².'),
	(502, '3 quartos, 2 suítes, varanda ampla com churrasqueira, 90m².'),
	(503, '3 quartos, suíte master com closet, 95m².'),
	(601, 'Cobertura duplex, 2 suítes, área externa com deck, 110m².'),
	(602, '3 quartos, cobertura com jacuzzi e área gourmet, 115m².')
;

-- aluguel dos apartamentos

INSERT INTO Aluguel(numero_apartamento, valor) values
	(101, 2000.00),
	(102, 1600.00),
	(103, 1700.00),
	(104, 1800.00),
	(201, 1650.00),
	(202, 1900.00),
	(203, 1950.00),
	(204, 2000.00),
	(301, 2100.00),
	(302, 2150.00),
	(303, 2300.00),
	(304, 2900.00),
	(401, 2400.00),
	(402, 2550.00),
	(403, 3000.00),
	(501, 3200.00),
	(502, 3400.00),
	(503, 3500.00),
	(601, 4500.00),
	(602, 4800.00)
;



--- # #  # # # Consultas: # # # #

-- Total pago por cada condômino:

SELECT 
  c.Nome_Condomino,
  c.CPF_Condomino,
  COUNT(p.ID_Pagamento) AS Num_Pagamentos,
  SUM(a.Valor) AS Total_Pago
FROM Pagamento p
JOIN Condomino c ON p.CPF_Condomino = c.CPF_Condomino
JOIN Apartamento a ON p.Numero_Apartamento = a.Numero_Apartamento
GROUP BY c.Nome_Condomino, c.CPF_Condomino;


-- Áreas comuns reservadas nos últimos 7 dias:

SELECT ac.Nome_Local, ac.Data_Reserva, c.Nome_Condomino
FROM Area_Comum ac
JOIN Condomino c ON ac.CPF_Condomino = c.CPF_Condomino
WHERE ac.Data_Reserva BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
ORDER BY ac.Data_Reserva;

-- Apartamentos vagos(sem nenhum inquilino:

SELECT a.Numero_Apartamento, a.Descricao_Comodo, a.Valor
FROM Apartamento a
WHERE a.CPF_Condomino IS NULL;

-- Histórico do Aluguel de um apartamento:

SELECT 
  a.Numero_Apartamento, 
  c.Nome_Condomino,
  al.Data_Entrada, 
  al.Data_Saida
FROM Aluguel al
JOIN Apartamento a ON al.Numero_Apartamento = a.Numero_Apartamento
LEFT JOIN Condomino c ON al.CPF_Condomino = c.CPF_Condomino
ORDER BY a.Numero_Apartamento, al.Data_Entrada;

-- Condôminos com recibos emitidos, mas que não pagaram o Aluguel do mês atual. I.e Alguém que costuma
-- pagar o Aluguel, mas ainda não enviou o deste mês.

SELECT 
  c.Nome_Condomino,
  c.CPF_Condomino,
  r.ID_Recibo,
  p.Data_Pagamento,
  a.Numero_Apartamento
FROM Recibo r
JOIN Pagamento p ON r.ID_Pagamento = p.ID_Pagamento
JOIN Condomino c ON r.CPF_Condomino = c.CPF_Condomino
JOIN Apartamento a ON p.Numero_Apartamento = a.Numero_Apartamento
WHERE DATE_TRUNC('month', p.Data_Pagamento) < DATE_TRUNC('month', CURRENT_DATE)
  AND c.CPF_Condomino NOT IN (
    SELECT DISTINCT CPF_Condomino
    FROM Pagamento
    WHERE DATE_TRUNC('month', Data_Pagamento) = DATE_TRUNC('month', CURRENT_DATE)
  )
ORDER BY c.Nome_Condomino;