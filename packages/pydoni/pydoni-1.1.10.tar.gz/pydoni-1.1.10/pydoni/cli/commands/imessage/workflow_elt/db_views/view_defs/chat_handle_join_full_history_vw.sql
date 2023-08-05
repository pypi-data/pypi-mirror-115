drop view if exists imessage_current.chat_handle_join_full_history_vw;

create or replace view imessage_current.chat_handle_join_full_history_vw as

select
    chat_handle_join.chat_id,
    chat_handle_join.handle_id,
    'imessage_current'::text as source
from
    imessage_current.chat_handle_join

union

select
    chat_handle_join_20191126.chat_id,
    chat_handle_join_20191126.handle_id,
    'imessage_20191126'::text as source
from
    imessage_historical.chat_handle_join_20191126

union

select
    chat_handle_join_20171001.chat_id,
    chat_handle_join_20171001.handle_id,
    'imessage_20171001'::text as source
from
    imessage_historical.chat_handle_join_20171001