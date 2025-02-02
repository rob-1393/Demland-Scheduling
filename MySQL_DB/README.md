# Adding the Database:


### Windows:
WARNING: The work for this has been done mainly from Debian-based Linux; I'll write out a proper installation guide for Windows later. For now:

1. Download the .sql file.
2. Reformat the file contents (remove apostrophes/backquotes where applicable, such as in table creation table statements).
3. Create a database (to contextualize the creation statements).
4. Run the SQL.

If you encounter problems, don't forget to ask for help in the server.

### Linux:

#### Installing necessary packages:
```
sudo apt update && sudo apt upgrade

sudo apt install libdbd-mysql-perl mysql-apt-config mysql-client mysql-common mysql-community-client mysql-community-client-core mysql-community-client-plugins mysql-community-server mysql-community-server-core
```

#### How to add the database:
Import:
```
mysql -u root -p DatabaseName < DatabaseFileName.sql
```

Export:
```
mysqldump -u root -p DatabaseName > DatabaseFileName.sql
```

 If the execution hangs, add "--single-transaction" after the database name flag (i.e.):
```
mysql -u root -p DatabaseName --single-transaction < DatabaseFileName.sql
mysqldump -u root -p DatabaseName --single-transaction > DatabaseFileName.sql
```
# Using the Conversion Script:

#### Linux:

The following creates a virtual environment for running pip. This may be unnecessary on other distributions. [Consider the README here](./ConversionScript).

```
sudo apt install python3-venv

python3 -m venv myenv

source myenv/bin/activate

pip install openpyxl sqlalchemy pandas mysql-connector-python
```
The "source" command here is used to enter the newly created environment.

