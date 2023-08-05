CREATE OR REPLACE VIEW imessage.contact_names_vw AS

 SELECT r2.chat_identifier,
    r2.contact_name
   FROM ( SELECT contact_names.chat_identifier,
            contact_names.contact_name
           FROM imessage.contact_names
        UNION
         SELECT contact_names_manual.chat_identifier,
            contact_names_manual.contact_name
           FROM imessage.contact_names_manual
        UNION
         SELECT r1.cache_roomnames AS chat_identifier,
            r1.group_title AS contact_name
           FROM ( SELECT DISTINCT message.cache_roomnames,
                    message.group_title,
                    row_number() OVER (PARTITION BY message.cache_roomnames ORDER BY message.date DESC) AS r
                   FROM imessage_current.message
                  WHERE message.cache_roomnames IS NOT NULL AND message.group_title IS NOT NULL) r1
          WHERE r1.r = 1) r2
  WHERE r2.chat_identifier IS NOT NULL;