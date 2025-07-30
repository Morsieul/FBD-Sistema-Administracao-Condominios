CREATE VIEW vw_proxima_reserva_por_condomino AS
SELECT DISTINCT ON (c.cpf_condomino)
  c.nome_condomino,
  c.cpf_condomino,
  r.data_reserva,
  ac.nome_local
FROM Condomino c
JOIN Reserva_Area r ON r.cpf_condomino = c.cpf_condomino
JOIN Area_Comum ac ON ac.id_area = r.id_area
WHERE r.data_reserva >= CURRENT_DATE
ORDER BY c.cpf_condomino, r.data_reserva;

CREATE VIEW vw_locacoes_ativas_com_pagamento_em_dia AS
SELECT
  c.nome_condomino,
  c.cpf_condomino,
  a.numero_apartamento,
  al.valor,
  al.data_entrada,
  al.data_saida,
  p.data_pagamento
FROM Aluguel al
JOIN Condomino c ON al.cpf_condomino = c.cpf_condomino
JOIN Apartamento a ON a.numero_apartamento = al.numero_apartamento
JOIN Pagamento p ON p.cpf_condomino = c.cpf_condomino
  AND p.numero_apartamento = a.numero_apartamento
WHERE CURRENT_DATE BETWEEN al.data_entrada AND al.data_saida
  AND DATE_TRUNC('month', p.data_pagamento) = DATE_TRUNC('month', CURRENT_DATE);

CREATE VIEW vw_historico_detalhado_por_apartamento AS
SELECT
  ap.numero_apartamento,
  ap.descricao_comodo,
  al.valor AS valor_aluguel,
  al.data_entrada,
  al.data_saida,
  c.nome_condomino,
  c.cpf_condomino,
  p.data_pagamento,
  ac.nome_local AS area_reservada,
  r.data_reserva
FROM Apartamento ap
LEFT JOIN Aluguel al ON al.numero_apartamento = ap.numero_apartamento
LEFT JOIN Condomino c ON c.cpf_condomino = al.cpf_condomino
LEFT JOIN Pagamento p ON p.numero_apartamento = ap.numero_apartamento AND p.cpf_condomino = c.cpf_condomino
LEFT JOIN Reserva_Area r ON r.cpf_condomino = c.cpf_condomino
LEFT JOIN Area_Comum ac ON ac.id_area = r.id_area
ORDER BY ap.numero_apartamento, al.data_entrada;

select * from vw_historico_detalhado_por_apartamento