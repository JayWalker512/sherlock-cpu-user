SherLock CPU User (Classifier)
------------------------------

This experiment aims to determine if it's possible to identify the user of a particular device based on their historical CPU usage patterns. It makes use of the SherLock dataset, which includes smartphone data from 50 users sampled over a 2-year period.

Note that I have not included the SherLock dataset here or extracted files due to licensing requirements, and the fact that the source files are many tens of gigabytes.

Requirements
------------

These scripts are written in Python 2.7 and make use of SciKit-Learn libraries as well as SQLite3. The easiest way to get the ML related libraries you'll need to run these scripts is by installing the Anaconda machine learning tool suite. See here: [https://www.anaconda.com/download/](https://www.anaconda.com/download/)

Usage
-----

The relevant file from the SherLock dataset to start with is **anon\_T4.tsv**. The process to extract features and follow it with classification is as follows:

**cpu_fields_feature_extract.py anon\_T4.tsv**

Using the above example command, the relevant fields (user_id, timestamp, cpu_total) will be extracted from the source dataset and put in a file called ** cpu_fields.tsv **. This is simply to reduce the size of the data we're working with and pull out the fields we're interested in.

**sherlock\_sql\_import.py cpu\_fields.tsv cpu\_field\_names.tsv** 

Use the above example command to import the source data into an SQLite3 database, which will be called ** export.db ** by default, as this is hardcoded in the script. The ** cpu\_field\_names.tsv ** file will determine the column names in this database, as column names are not included in the source data file. In this case they will be ** cpu_total	timestamp	user **.

**generate\_classifier\_features\_from\_db.py export.db**

This script will read the database you created with the last script, and extract our selection of statistical features using SQL queries and some other field conversions. This script will create the file ** cpu\_classifier\_features.tsv ** which is the input to our final script, the classifier.

**cpu\_user\_classifier.py cpu\_classifier\_features.tsv**

This script will train basic neural network to classify a user by the CPU usage features we extracted in the previous steps. It will give an accuracy percentage, F1 score, and a learning curve image.




