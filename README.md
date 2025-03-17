# Advanced Programming - Group-01
This repository contains the group project of group 01 for the advanced programming course.

Michel
64827@novasbe.pt

Konstantin
67864@novasbe.pt

Simon
63545@novasbe.pt

Vinzent
65479@novasbe.pt

## Instructions
### Set up Environment (optional)
**Create Conda Environment**
```
conda env create -f environment.yml
```
**Activate the Environment**
```
conda activate adpro
```

### Install Requirements
A full list of all dependencies installed during implementation of the project can be found in the requirements.txt file in the main directory. 

Run the following command to install everything: 
```
pip install -r requirements.txt
```
if you do not have pip installed, run this first:
```
conda install pip
```
### Install and run LLM
To run the local LLM you must first install [Ollama](https://ollama.com/).

Then, download the Deepseek R1 model with 1.5b Tokens [DeepSeek R1](https://ollama.com/library/deepseek-r1:1.5b). 

Before running the app make sure that Ollama is running in the background. 

### Running the app
To run the application, use the following command in the main directory: 
```
./run_app.sh 
```
To run tests, use:
```
pytest
````

## Essay: How Text Classification could help with the UN's SDGs

The text classification component of this project, which uses natural language processing to classify movie genres based on their summaries and titles, has promising potential for supporting the United Nations Sustainable Development Goals (SDGs). Through its analytical capabilities, this system can be applied in educational settings to help students and teachers identify relevant films aligned with curricular goals, thereby promoting quality education (SDG 4). Furthermore, it can play a pivotal role in advocating for gender equality (SDG 5) by assessing the representation of genders in media, highlighting films with balanced and inclusive portrayals.

Additionally, this classification approach could serve to reduce inequalities (SDG 10) by identifying and encouraging diverse storytelling, ensuring cultural and ethnic groups receive equitable representation in global media. The project’s capacity for analyzing the evolution of cultural themes through movies also supports the preservation of heritage and community identity, directly aligning with SDG 11 (sustainable cities and communities). Lastly, by leveraging genre and thematic analysis, this technology could help strengthen public institutions (SDG 16) by identifying films addressing critical social issues, contributing to a culture of peace, justice, and reliable information dissemination.

Overall, applying intelligent text classification to media analysis not only enhances our understanding of film content but also positions entertainment as a proactive partner in achieving sustainable global development.

