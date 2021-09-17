BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users" (
	"access"	INTEGER,
	"name"	TEXT,
	"id"	INTEGER,
	"nic"	TEXT,
	"firs_name"	TEXT,
	"last_name"	TEXT,
	"timer"	TEXT
);
COMMIT;
