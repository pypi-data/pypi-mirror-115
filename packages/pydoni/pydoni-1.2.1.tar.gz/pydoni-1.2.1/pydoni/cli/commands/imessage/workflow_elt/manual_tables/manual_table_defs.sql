-- Rebuilt from data stored in table_data/
drop table if exists imessage.contact_names_ignored cascade;
create table imessage.contact_names_ignored (
    chat_identifier text,
    notes text
);

-- Rebuilt from data stored in table_data/
drop table if exists imessage.contact_names_manual cascade;
create table imessage.contact_names_manual (
    chat_identifier text,
    contact_name text
);

create table if not exists imessage.contact_names (
    chat_identifier text,
    contact_name text
);
