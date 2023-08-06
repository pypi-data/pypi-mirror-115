drop view if exists imessage_current.message_full_history_vw;

create or replace view imessage_current.message_full_history_vw as

select
    map.message_uid
    , m."ROWID"
    , m.guid
    , m.text
    , 'imessage_current'::text as source
    , m.replace
    , m.service_center
    , m.handle_id
    , m.subject
    , m.country
    , m."attributedBody"
    , m.version::text as version
    , m.type::text as type
    , m.service
    , m.account
    , m.account_guid
    , m.error
    , to_timestamp(((m.date::double precision / 1000000000::double precision)::numeric + '978307200'::numeric)::double precision) as date
    , m.date as date_ts
    , m.date_read
    , m.date_delivered
    , m.is_delivered
    , m.is_finished
    , m.is_emote
    , m.is_from_me
    , m.is_empty
    , m.is_delayed
    , m.is_auto_reply
    , m.is_prepared
    , m.is_read
    , m.is_system_message
    , m.is_sent
    , m.has_dd_results
    , m.is_service_message
    , m.is_forward
    , m.was_downgraded
    , m.is_archive
    , m.cache_has_attachments
    , m.cache_roomnames
    , m.was_data_detected
    , m.was_deduplicated
    , m.is_audio_message
    , m.is_played
    , m.date_played
    , m.item_type
    , m.other_handle
    , m.group_title
    , m.group_action_type
    , m.share_status
    , m.share_direction
    , m.is_expirable
    , m.expire_state
    , m.message_action_type
    , m.message_source
    , m.associated_message_guid
    , m.associated_message_type
    , m.balloon_bundle_id
    , m.payload_data
    , m.expressive_send_style_id
    , m.associated_message_range_location
    , m.associated_message_range_length
    , m.time_expressive_send_played
    , m.message_summary_info
    , m.ck_sync_state
    , m.ck_record_id
    , m.ck_record_change_tag
    , m.destination_caller_id
    , m.sr_ck_sync_state
    , m.sr_ck_record_id
    , m.sr_ck_record_change_tag
    , m.is_corrupt
    , m.reply_to_guid
    , m.sort_id
    , m.is_spam
    , m.has_unseen_mention
    , m.thread_originator_guid
    , m.thread_originator_part
from
    imessage_current.message m
    left join
        imessage_current.map_message_id map
        on m."ROWID" = map."ROWID"
        and map.source::text = 'imessage_current'::text

union

select
    map.message_uid
    , m."ROWID"
    , m.guid
    , m.text
    , 'imessage_20191126'::text as source
    , m.replace
    , m.service_center
    , m.handle_id
    , m.subject
    , m.country
    , m."attributedBody"
    , m.version::text as version
    , m.type::text as type
    , m.service
    , m.account
    , m.account_guid
    , m.error
    , to_timestamp(((m.date::double precision / 1000000000::double precision)::numeric + '978307200'::numeric)::double precision) as date
    , m.date as date_ts
    , m.date_read
    , m.date_delivered
    , m.is_delivered
    , m.is_finished
    , m.is_emote
    , m.is_from_me
    , m.is_empty
    , m.is_delayed
    , m.is_auto_reply
    , m.is_prepared
    , m.is_read
    , m.is_system_message
    , m.is_sent
    , m.has_dd_results
    , m.is_service_message
    , m.is_forward
    , m.was_downgraded
    , m.is_archive
    , m.cache_has_attachments
    , m.cache_roomnames
    , m.was_data_detected
    , m.was_deduplicated
    , m.is_audio_message
    , m.is_played
    , m.date_played
    , m.item_type
    , m.other_handle
    , m.group_title
    , m.group_action_type
    , m.share_status
    , m.share_direction
    , m.is_expirable
    , m.expire_state
    , m.message_action_type
    , m.message_source
    , m.associated_message_guid
    , m.associated_message_type
    , m.balloon_bundle_id
    , m.payload_data
    , m.expressive_send_style_id
    , m.associated_message_range_location
    , m.associated_message_range_length
    , m.time_expressive_send_played
    , m.message_summary_info
    , m.ck_sync_state
    , m.ck_record_id
    , m.ck_record_change_tag
    , m.destination_caller_id
    , m.sr_ck_sync_state
    , m.sr_ck_record_id
    , m.sr_ck_record_change_tag
    , m.is_corrupt
    , m.reply_to_guid
    , m.sort_id
    , m.is_spam
    , null::bigint as has_unseen_mention
    , null::text as thread_originator_guid
    , null::text as thread_originator_part
from
    imessage_historical.message_20191126 m
    left join
        imessage_current.map_message_id map
        on m."ROWID" = map."ROWID"
        and map.source::text = 'imessage_20191126'::text

union

select
    map.message_uid
    , m."ROWID"
    , m.guid
    , m.text
    , 'imessage_20171001'::text as source
    , m.replace
    , m.service_center::text as service_center
    , m.handle_id
    , m.subject
    , m.country::text as country
    , m."attributedBody"
    , m.version
    , m.type
    , m.service
    , m.account
    , m.account_guid
    , m.error
    , case
          when (to_timestamp(m.date) + '31 years'::interval + '1 day'::interval) < '2016-02-29 00:00:00-06'::timestamp with time zone
          then to_timestamp(m.date) + '31 years'::interval + '1 day'::interval
          else to_timestamp(m.date) + '31 years'::interval
      end as date
    , m.date as date_ts
    , m.date_read
    , m.date_delivered
    , m.is_delivered
    , m.is_finished
    , m.is_emote
    , m.is_from_me
    , m.is_empty
    , m.is_delayed
    , m.is_auto_reply
    , m.is_prepared
    , m.is_read
    , m.is_system_message
    , m.is_sent
    , m.has_dd_results
    , m.is_service_message
    , m.is_forward
    , m.was_downgraded
    , m.is_archive
    , m.cache_has_attachments
    , m.cache_roomnames
    , m.was_data_detected
    , m.was_deduplicated
    , m.is_audio_message
    , m.is_played
    , m.date_played
    , m.item_type
    , m.other_handle
    , m.group_title
    , m.group_action_type
    , m.share_status
    , m.share_direction
    , m.is_expirable
    , m.expire_state
    , m.message_action_type
    , m.message_source
    , m.associated_message_guid
    , m.associated_message_type
    , m.balloon_bundle_id
    , m.payload_data
    , m.expressive_send_style_id
    , m.associated_message_range_location
    , m.associated_message_range_length
    , m.time_expressive_send_played
    , m.message_summary_info
    , null::bigint as ck_sync_state
    , null::text as ck_record_id
    , null::text as ck_record_change_tag
    , null::text as destination_caller_id
    , null::bigint as sr_ck_sync_state
    , null::text as sr_ck_record_id
    , null::text as sr_ck_record_change_tag
    , null::bigint as is_corrupt
    , null::text as reply_to_guid
    , null::bigint as sort_id
    , null::bigint as is_spam
    , null::bigint as has_unseen_mention
    , null::text as thread_originator_guid
    , null::text as thread_originator_part
from
    imessage_historical.message_20171001 m
    left join
        imessage_current.map_message_id map
        on m."ROWID" = map."ROWID"::double precision
        and map.source::text = 'imessage_20171001'::text
order by
    18 desc  -- Order by "date"