CREATE OR REPLACE VIEW imessage_current.chat_message_join_full_history_vw AS

 SELECT chat_message_join.chat_id,
    chat_message_join.message_id,
    chat_message_join.message_date,
    'imessage_current'::text AS source
   FROM imessage_current.chat_message_join
UNION
 SELECT chat_message_join_20191126.chat_id,
    chat_message_join_20191126.message_id,
    chat_message_join_20191126.message_date,
    'imessage_20191126'::text AS source
   FROM imessage_historical.chat_message_join_20191126
UNION
 SELECT chat_message_join_20171001.chat_id,
    chat_message_join_20171001.message_id,
    NULL::bigint AS message_date,
    'imessage_20171001'::text AS source
   FROM imessage_historical.chat_message_join_20171001;