CREATE TABLE IF NOT EXISTS "Container"(
    "Name" TEXT PRIMARY KEY NOT NULL UNIQUE,
    "Hosted" TEXT NOT NULL UNIQUE,
    "Version" VARCHAR(20) NOT NULL,
    "Readme" TEXT DEFAULT "",
    "Default" BOOL DEFAULT FALSE
);


INSERT OR IGNORE INTO "Container"(
    "Name", "Hosted", "Version", "Default") VALUES (
    "Rash", "https://github.com/RahulARanger/Rash/tree/master/Rash", "0.0.4", TRUE
);


INSERT OR IGNORE INTO "Container"(
"Name", "Hosted", "Version", "Default") VALUES (
"RashLogger", "https://github.com/RahulARanger/Rash/tree/master/RashLogger/RashLogger", "0.0.1", TRUE
);

CREATE TABLE IF NOT EXISTS "Sql"(
    "Hash" INT PRIMARY KEY NOT NULL UNIQUE,
    "SQL" TEXT NOT NULL,
    "Empty" BOOLEAN NOT NULL DEFAULT TRUE
);


INSERT OR IGNORE INTO "Sql"(
'Hash', 'SQL', "Empty") VALUES(
0, "SELECT SQL, Empty FROM Sql WHERE Hash = ?", FALSE
);


INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL") VALUES (
1, "SELECT Name, Hosted, Version, 'Default' FROM Container;"
); -- for selecting all entities except markdown in Container


INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL", "Empty") VALUES (
2, "SELECT Hosted, Version, 'Default' FROM Container WHERE Name = ?;", FALSE
); -- searches in container through Name column


INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL", "Empty") VALUES (
3, "SELECT Hosted FROM Container WHERE Name = ?;", False
);

INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL", "Empty") VALUES (
4, "SELECT Version FROM Container WHERE Name = ?;", False
);

INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL") VALUES (
5, "SELECT Name FROM Container;"
);

INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL") VALUES (
6, 'SELECT Name FROM Container WHERE "Name" <> "Rash";'
);


INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL", "Empty") VALUES (
7, "SELECT Readme FROM Container WHERE Name = ?;", False
);


INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL", "Empty") VALUES(
8, "UPDATE Container SET Version = ? WHERE Name = ?;", False
);

INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL", "Empty") VALUES(
9, "UPDATE Container SET Readme = ? WHERE Name = ?;", False
);

INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL", "Empty") VALUES(
10, "INSERT INTO Sql(Name, Hosted, Version, Readme) VALUES(?, ?, ?, ?);", False
);

INSERT OR IGNORE INTO "Sql"(
"Hash", "SQL", "Empty") VALUES(
11, "SELECT Name FROM Container WHERE Hosted = ?", False
);