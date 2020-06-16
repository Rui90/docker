create database email_sender;

\c email_sender

create table emails (
    id serial not null,
    data timestamp not null default CURRENT_TIMESTAMP, 
    subject varchar(100) not null,
    body varchar(250) not null
);

