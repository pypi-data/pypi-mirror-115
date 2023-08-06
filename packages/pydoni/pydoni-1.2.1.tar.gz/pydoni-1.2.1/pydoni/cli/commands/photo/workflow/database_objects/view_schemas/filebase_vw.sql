create or replace view photo.filebase_vw as
select
	fpath,
	ftype,
	fsize,
	fmod_ts
from (
	select
		fpath,
		ftype,
		fsize,
		fmod_ts,
		logged_ts,
		row_number() over(partition by fpath order by logged_ts desc) as r
	from
		photo.filebase_history
) t1
where
	r = 1