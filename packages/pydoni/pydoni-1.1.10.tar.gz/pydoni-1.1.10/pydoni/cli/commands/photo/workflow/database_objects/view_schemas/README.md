# Database Views

> Record metadata about each view defined in the `photo` database.

- `filebase_vw`: Most recently logged record for each fpath in `photo.filebase_history`. An fpath can appear multiple times in `filebase_history`, so this view selects only the latest logged record for each fpathm which yields that file's most recent size, modification time, etc. Unique on fpath.