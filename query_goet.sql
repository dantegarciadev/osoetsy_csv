SELECT count(*) FROM goet.usuarios;


SELECT 
  table_name, 
  table_rows,
  AUTO_INCREMENT

FROM 
  information_schema.tables 
WHERE 
  table_schema = 'goet';