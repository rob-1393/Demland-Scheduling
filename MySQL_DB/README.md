# Using the MySQL Database:

## Installation of MySQL:

### Windows:

1. Download MySQL Server [here](https://dev.mysql.com/downloads/mysql/).
2. Download MySQL Community Workbench [here](https://dev.mysql.com/downloads/workbench/).
3. Set up a local MySQL Server & Workbench. The following guide might help [here](https://www.youtube.com/watch?v=u96rVINbAUI).

### Linux:

Install the MySQL repo (eg. [the apt repo](https://dev.mysql.com/downloads/repo/apt/)).

```
sudo apt update && sudo apt upgrade

sudo apt install libdbd-mysql-perl mysql-apt-config mysql-client mysql-common mysql-community-client mysql-community-client-core mysql-community-client-plugins mysql-community-server mysql-community-server-core
```
Note: The guide in the Windows section might be useful for MySQL configurations.

## Importing/Exporting (OS Agnostic):

1. Create a database:
```
mysql -u root -p

mysql> create database DatabaseName;
mysql> show databases;
```
Please note that upon the original installation, you might need to set up user access to MySQL. Alternatively, running `mysql` as Administrator  or root should work.

#### Import:
```
mysql -u root -p DatabaseName < DatabaseFileName.sql
```

#### Export:
```
mysqldump -u root -p DatabaseName > DatabaseFileName.sql
```

If the execution hangs, add "--single-transaction" after the database name flag (or the name itself).

# Using the Conversion Script:

### Linux:

The following creates a virtual environment for running pip. This may be unnecessary on other distributions. [Consider the README here](./ConversionScript).

```
sudo apt install python3-venv

python3 -m venv myenv

source myenv/bin/activate

pip install openpyxl sqlalchemy pandas mysql-connector-python
```
The "source" command here is used to enter the newly created environment.

