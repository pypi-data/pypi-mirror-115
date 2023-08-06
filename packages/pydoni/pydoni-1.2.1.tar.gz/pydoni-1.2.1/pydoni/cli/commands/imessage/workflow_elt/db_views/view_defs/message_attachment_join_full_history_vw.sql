drop view if exists imessage_current.message_attachment_join_full_history_vw;

create or replace view imessage_current.message_attachment_join_full_history_vw as

select
    message_id
    , attachment_id
    , 'imessage_current' as source
from
    imessage_current.message_attachment_join

union

select
    message_id
    , attachment_id
    , 'imessage_20191126' as source
from
    imessage_historical.message_attachment_join_20191126

union

select
    message_id
    , attachment_id
    , 'imessage_20171001' as source
from
    imessage_historical.message_attachment_join_20171001;