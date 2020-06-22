# docker-genome
Docker-based project to read variant data from .vcf files, insert it into a database, and then search said database for specific variants.

'db' contains the initialisation for the mySQL database.
'fillDB' contains the variant data for the database, as well as a Python script to insert this data.
'readDB' contains the input filters, as well as a Python script to retrieve the desired data from the database and output this onto the website.
Note that the docker-compose.yml links the three folders via dependencies, requiring them to activate in the correct order: first the database, then fillDB, and readDB last.

Further comments are placed in the Python scripts.
