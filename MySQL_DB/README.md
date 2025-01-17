# Warning:
I have not tested any of this on any non-debian-based Linux distribution, nor Windows or MacOS, so I wouldn't be surprised if the commands are slightly different.

# How to add the database:
`mysql -u root -p DatabaseName < DatabaseFileName.sql`

The command to make a MySQL database into a file reverses the "<" and uses the "mysqldump" command.

`mysqldump -u root -p DatabaseName > DatabaseFileName.sql`

 If the execution hangs, add "--single-transaction" after the other flags (-p).
