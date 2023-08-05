# Photo ELT Workflow

## The Pipeline

### Extract

The workflow begins by pulling file metadata from files on the local filesystem. The files are considered the primary source of data in the target database, so this workflow may only be run when those local media files are accessible. A file list is generated using a supplied directory path, and the files in the supplied directory are scanned for metadata attributes, such as last modification time, size, etc.

### Load

Once data has been extracted from the source local media files, that data is compared with what currently xists in the database, if at all.

### Transform

## The Dashboard