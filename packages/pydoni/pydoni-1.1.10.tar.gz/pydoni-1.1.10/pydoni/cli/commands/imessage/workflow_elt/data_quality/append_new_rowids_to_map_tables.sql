--
-- Attachment
--

insert into {pg_schema_load}.map_attachment_id ("ROWID", source)
select attachment."ROWID", 'imessage_current' as source
from {pg_schema_load}.attachment attachment
left join {pg_schema_load}.map_attachment_id map
       on attachment."ROWID" = map."ROWID"
      and map.source = 'imessage_current'
where map."ROWID" is null
  and attachment."ROWID" is not null;

insert into {pg_schema_load}.map_attachment_id ("ROWID", source)
select attachment."ROWID", 'imessage_20191126' as source
from imessage_historical.attachment_20191126 attachment
left join {pg_schema_load}.map_attachment_id map
       on attachment."ROWID" = map."ROWID"
      and map.source = 'imessage_20191126'
where map."ROWID" is null
  and attachment."ROWID" is not null;

insert into {pg_schema_load}.map_attachment_id ("ROWID", source)
select attachment."ROWID", 'imessage_20171001' as source
from imessage_historical.attachment_20171001 attachment
left join {pg_schema_load}.map_attachment_id map
       on attachment."ROWID" = map."ROWID"
      and map.source = 'imessage_20171001'
where map."ROWID" is null
  and attachment."ROWID" is not null;

--
-- Chat
--

insert into {pg_schema_load}.map_chat_id ("ROWID", source)
select chat."ROWID", 'imessage_current' as source
from {pg_schema_load}.chat chat
left join {pg_schema_load}.map_chat_id map
       on chat."ROWID" = map."ROWID"
      and map.source = 'imessage_current'
where map."ROWID" is null
  and chat."ROWID" is not null;

insert into {pg_schema_load}.map_chat_id ("ROWID", source)
select chat."ROWID", 'imessage_20191126' as source
from imessage_historical.chat_20191126 chat
left join {pg_schema_load}.map_chat_id map
       on chat."ROWID" = map."ROWID"
      and map.source = 'imessage_20191126'
where map."ROWID" is null
  and chat."ROWID" is not null;

insert into {pg_schema_load}.map_chat_id ("ROWID", source)
select chat."ROWID", 'imessage_20171001' as source
from imessage_historical.chat_20171001 chat
left join {pg_schema_load}.map_chat_id map
       on chat."ROWID" = map."ROWID"
      and map.source = 'imessage_20171001'
where map."ROWID" is null
  and chat."ROWID" is not null;

--
-- Handle
--

insert into {pg_schema_load}.map_handle_id ("ROWID", source)
select handle."ROWID", 'imessage_current' as source
from {pg_schema_load}.handle handle
left join {pg_schema_load}.map_handle_id map
       on handle."ROWID" = map."ROWID"
      and map.source = 'imessage_current'
where map."ROWID" is null
  and handle."ROWID" is not null;

insert into {pg_schema_load}.map_handle_id ("ROWID", source)
select handle."ROWID", 'imessage_20191126' as source
from imessage_historical.handle_20191126 handle
left join {pg_schema_load}.map_handle_id map
       on handle."ROWID" = map."ROWID"
      and map.source = 'imessage_20191126'
where map."ROWID" is null
  and handle."ROWID" is not null;

insert into {pg_schema_load}.map_handle_id ("ROWID", source)
select handle."ROWID", 'imessage_20171001' as source
from imessage_historical.handle_20171001 handle
left join {pg_schema_load}.map_handle_id map
       on handle."ROWID" = map."ROWID"
      and map.source = 'imessage_20171001'
where map."ROWID" is null
  and handle."ROWID" is not null;

--
-- Message
--

insert into {pg_schema_load}.map_message_id ("ROWID", source)
select message."ROWID", 'imessage_current' as source
from {pg_schema_load}.message message
left join {pg_schema_load}.map_message_id map
       on message."ROWID" = map."ROWID"
      and map.source = 'imessage_current'
where map."ROWID" is null
  and message."ROWID" is not null;

insert into {pg_schema_load}.map_message_id ("ROWID", source)
select message."ROWID", 'imessage_20191126' as source
from imessage_historical.message_20191126 message
left join {pg_schema_load}.map_message_id map
       on message."ROWID" = map."ROWID"
      and map.source = 'imessage_20191126'
where map."ROWID" is null
  and message."ROWID" is not null;

insert into {pg_schema_load}.map_message_id ("ROWID", source)
select message."ROWID", 'imessage_20171001' as source
from imessage_historical.message_20171001 message
left join {pg_schema_load}.map_message_id map
       on message."ROWID" = map."ROWID"
      and map.source = 'imessage_20171001'
where map."ROWID" is null
  and message."ROWID" is not null;
