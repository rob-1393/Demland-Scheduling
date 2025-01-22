# Warning:
Mainly working from Debian here. On Windows I recommend downloading the .sql file, reformatting the file contents, manually creating a database to use for the creation statements, and then running the script. I'll write out a proper installation guide for Windows later.

# (Debian-based Linux) Installation of necessary packages:
`sudo apt update && sudo apt upgrade`
`sudo apt install libdbd-mysql-perl mysql-apt-config mysql-client mysql-common mysql-community-client mysql-community-client-core mysql-community-client-plugins mysql-community-server mysql-community-server-core`

# How to add the database:
`mysql -u root -p DatabaseName < DatabaseFileName.sql`

The command to make a MySQL database into a file reverses the "<" and uses the "mysqldump" command.

`mysqldump -u root -p DatabaseName > DatabaseFileName.sql`

 If the execution hangs, add "--single-transaction" after the other flags (-p DatabaseName <here>).
