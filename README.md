# Linkedin skill assessments quizzes

## About the repository

This repository contains the source data of QuizGame. Each topics is organized into a folder that contains the English markdown file of questions and the images included in the markdown files.

## Settings

In order to include this repository into a MAUI project, the `file_modifier.py` script should be run to initialize it. It doesn't requires any special library beside standard python libraries.  

#### Parameter description

The script accepts one parameter that describes which type of directory should be initialized. Basically, the parameter is a boolean type and the valid inputs are:
* `['true', '1', 't', 'y', 'yes']` for true value
    * This will initialize the directory as raw resource (.md files are included). Should be placed into `Resources/Raw` folder of the MAUI project.
* `['false', '0', 'f', 'n', 'no']` for false value
    * This will initialize the directory as image resource (image files are included). Should be placed into `Resources/Images` folder of MAUI project.