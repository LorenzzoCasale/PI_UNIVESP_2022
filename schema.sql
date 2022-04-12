
DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

DROP TABLE IF EXISTS filter_sel;
CREATE TABLE filter_sel(
    selection TEXT NOT NULL
);

drop view if exists Resultados;
CREATE VIEW Resultados as
SELECT content AS Bairros, count(*) AS Ocorrências FROM posts group by (content) ORDER BY Ocorrências DESC;

drop view if exists Res_filtro;
CREATE VIEW Res_filtro as
SELECT content AS Bairros, count(created<=current_date-30) AS Ocorrências FROM posts, filter_sel where selection="Último Mês" group by (content) ORDER BY Ocorrências DESC;
