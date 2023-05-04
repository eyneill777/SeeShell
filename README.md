# SeeShell

SeeShell is a project that uses machine learning to identify shell species from user-uploaded images. SeeShell consists of two parts, a webserver (back end) and an android application (front end).  The server consists of an API, a MySQL Database, and a data lake containing seashell images. TODO write about client after specific technologies are decided.

## Getting started
Follow the instructions below to set up the server environment, database, data, and API for SeeShell.

### Environment Setup:
  - Install python 3
  - in the command line navigate to the source code folder, run the commands `cd Server` then `pip install -r server_requirements.txt`.  Then run the commands `cd ../Client` then `pip install -r client_requirements.txt`.  This will install the needed python libraries.
  - Download and install [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) and [MySQL Server](https://dev.mysql.com/downloads/mysql/)

### Database Setup
  - Ensure that the MySQL Server service is running. You can usually start the service from the MySQL Workbench or via system services.
  - Open MySQL Workbench and create a new database named "seeshell".
  - Open the config.json files in both the API and database folders, and update the "password" field with your MySQL root password.
  - In the repository, navigate to the database folder and run the generatetables.py file with the following command: `python generatetables.py`
    * This will generate the required tables in the "seeshell" database.

### Data Setup:
  - Download the shell dataset here and unzip it to a folder:
      https://springernature.figshare.com/articles/dataset/all_shell_images/9122621?backTo=/collections/A_shell_dataset_for_shell_features_extraction_and_recognition/4428335
  - edit config.json
    * Set rawDataPath to be the filepath to the shell data folder
    * Set genusPath and speciesPath to be locations of the output folders for preprocessed shell images.  These should be empty folders, and the preprocessing script will sort the data into them.
  - run PreprocessData.py

### Launch the API:
  - Navigate to the API folder in your repository in a terminal window
  - Type flask --app SeeShellAPI.py run to launch the API         (dev environment only)
