DROP TABLE IF EXISTS url;
CREATE TABLE url (
  id INTEGER PRIMARY KEY AUTOINCREMENT ,
  short_url TEXT NOT NULL,
  long_url TEXT NOT NULL
);
   