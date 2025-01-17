# Warning:
I have not tested any of this on any non-debian-based distribution, nor Windows or MacOS, so I wouldn't be surprised if the commands are slightly different.

# How to add the database:
`mysql -u root -p DatabaseName < DatabaseFileName.sql`

The command to make a MySQL database into a file reverses the "<", adds the single-transaction flag, and uses the "mysqldump" command.

`mysqldump -u root -p --single-transaction DatabaseName > DatabaseFileName.sql`
