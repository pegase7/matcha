create role matchaadmin password 'matchapass';
ALTER ROLE matchaadmin WITH LOGIN;
CREATE DATABASE matchadb OWNER matchaadmin;

