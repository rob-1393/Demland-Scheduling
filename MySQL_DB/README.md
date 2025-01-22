# Windows Warning:
I'm mainly working from Debian here; I'll write out a proper installation guide for Windows later. For now:

1. Download the .sql file.
2. Reformat the file contents (remove apostrophes/backquotes where applicable, such as in table creation table statements).
3. Create a database to contextualize the creation statements.
4. Run the script.

# (Debian-based Linux) Installation of necessary packages:
`sudo apt update && sudo apt upgrade`

`sudo apt install libdbd-mysql-perl mysql-apt-config mysql-client mysql-common mysql-community-client mysql-community-client-core mysql-community-client-plugins mysql-community-server mysql-community-server-core`

# (CLI) How to add the database:
`mysql -u root -p DatabaseName < DatabaseFileName.sql`

The command to make a MySQL database into a file reverses the "<" and uses the "mysqldump" command.

`mysqldump -u root -p DatabaseName > DatabaseFileName.sql`

 If the execution hangs, add "--single-transaction" after the other flags (-p DatabaseName <here>).
