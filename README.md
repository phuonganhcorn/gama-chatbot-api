# GAMA Chatbot
---
- _A little demo with chatbot_
  
![_**A little demo with chatbot**_](https://i.imgur.com/nNAP7Aa.png)

---


## Overview 

> [!NOTE]
> - This repository utilizes the API key from Gemini. To obtain your API key, please visit [Google AI Studio](https://ai.google.dev/tutorials/workspace_auth_quickstart).
> - This repository contains LICENSE from Apache License 2.0.

The GAMA Chatbot is designed to be a chatbot specifically tailored for GAMA. It _**leverages the API key from Google's Gemini chatbot service to provide intelligent responses to user queries related to GAMA topics.**_

---
## Purpose
The primary purpose of the GAMA Chatbot is to Create a beginner-friendly introduction/help to the GAML language to help new GAMA users get acquainted.

---
## Implementation
The GAMA Chatbot is implemented using Python programming language and various libraries and frameworks, including ```Streamlit``` for the user interface and the ```Google Gemini Chatbot API``` for natural language processing capabilities.

_First, clone this repository to your computer and then follow the instructions below._
### Step 1: Creat virtual/conda environment
- _With virtual environment_
```
python -m venv gemini-chatbot
source gemini-chatbot/bin/activate #for ubuntu
gemini-chatbot/Scripts/activate #for windows
```
- _With conda environment_
```
conda create --name gemini-chatbot
```
_After the installation, run command below to activate conda environment_
```
conda activate gemini-chatbot
```

### Step 2: Install libraries
```
cd ./gama-chatbot-api
pip install -r requirements.txt
```

### Step 3: Run chatbot interface with Streamlit
```
streamlit run app.py
```
---

> [!NOTE]
> - This chatbot right now just answer to questions related to questions related to GAMA platform in English, this is because of ```keywords.txt```. Users can modify this with English keywords or any other languages.
> - To ensure that the model responds only within the scope of GAMA, I have created a file containing keywords related to the GAMA platform. Users can update ```keywords.txt``` file after cloning this repository to enhance the accuracy/flexibility of the chatbot.
