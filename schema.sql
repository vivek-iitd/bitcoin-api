--sqlite3 historical.db < historical-schema.sql
drop table if exists bitcoin;
create table bitcoin (
	dt char(8) PRIMARY KEY,
	price decimal(8,1),
	open decimal(8,1),
	high decimal(8,1),
	low decimal(8,1),
	volume text,
	change text);
