# GAF API

An API for The Never Ending GAF  
**Website:** http://www.neverendinggaf.com  
**Current API Version:** `v3`

## Requirements
- Python 3.5+
- A PostgreSQL DB
- Gunicorn (or another WSGI server)
- Nginx (or another webserver)

#### Database Tables
Requires a PostgresSQL DB with the following tables

**Table Name:** `users`

Field Name | Data Type
--- | ---
user_id | int
access_token | text
refresh_token | text
country_code | text

**Table Name:** acronyms

Field Name | Data Type
--- | ---
id | serial
acronym | text
