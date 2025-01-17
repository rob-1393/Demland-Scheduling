# Warning:
Having a relational database file on github like this is very weird, but I think this will work.
Additionally, I have not tested any of this on any non-debian-based distribution, nor Windows or MacOS.

#### How to add the database:

`mysqldump -u root -p --single-transaction DatabaseName > DatabaseFileName.sql`

The command to add a MySQL database from a file reverses the ">", removes the single-transaction flag, and uses the standard "mysql" command.

`mysql -u root -p DatabaseName < DatabaseFileName.sql`
