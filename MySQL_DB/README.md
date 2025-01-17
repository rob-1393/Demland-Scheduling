# Warning:
Having a relational database file on github like this is very weird, but I think this will work.
Additionally, I have not tested any of this on any non-debian-based distribution, nor Windows or MacOS.

#### How to add the database:

`mysql -u root -p GCUScheduling < GCUScheduling_backup.sql`

The command to backup a database into a file is similar:

`mysql -u root -p GCUScheduling > GCUScheduling_backup.sql`
