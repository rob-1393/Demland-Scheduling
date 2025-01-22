# Warning:
I have not tested any of this on anything not Debian, but I believe everything should work fine.

# How to add the database (Debian):
`mysql -u root -p DatabaseName < DatabaseFileName.sql`

The command to make a MySQL database into a file reverses the "<" and uses the "mysqldump" command.

`mysqldump -u root -p DatabaseName > DatabaseFileName.sql`

 If the execution hangs, add "--single-transaction" after the other flags (-p).
