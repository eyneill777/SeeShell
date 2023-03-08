# SeeShell

Environment Setup:
  - Install python 3
  - in the command line navigate to the source code folder and run the command "pip install requirements.txt".  This will install the needed python libraries.


Server Setup:
  #Data Setup:
    - Download the shell dataset here and unzip it to a folder:
      https://springernature.figshare.com/articles/dataset/all_shell_images/9122621?backTo=/collections/A_shell_dataset_for_shell_features_extraction_and_recognition/4428335
    - edit config.json
      * Set rawDataPath to be the filepath to the shell data folder
      * Set genusPath and speciesPath to be locations of the output folders for preprocessed shell images.  These should be empty folders, and the preprocessing script will sort the data into them.
    - run PreprocessData.py
