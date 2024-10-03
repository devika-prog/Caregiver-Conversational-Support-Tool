# Caregiver Conversational Support Tool (CCST)
This repository contains the prompts used while designing the CCST, an LLM-integrated intelligent tutoring system with parent-student chat functionality.

[promptEngineeringExperiments.py](promptEngineeringExperiments.py) is a modified portion of the code from our server architecture that involves gathering different contextual information and assembling them into a prompt. 

The purpose of providing this code is for users to understand how supplying different values of contextual information provided to the prompt for an LLM results in different characteristics of generated message recommendations.

Only modify the code in the portion labeled TODO FOR USER. Users can modify the values in the variables labeled:
   - chat_message
   - next_step
   - student_hint
   - student_accuracy
   - question

Ensure that Python is installed (version 3.7 or later is recommended).

### Setup Instructions

1. Clone the repository, then cd into folder.

Install required dependencies before running:
1. Download [Ollama]([docs/CONTRIBUTING.md](https://ollama.com/download/mac))
3. Create a virtual environment (recommended)
   
    - To create:
           
            python -m venv .venv 
        
    - To activate (macOS/Linux):
    
          source .venv/bin/activate
    - To activate (Windows):

            venv\Scripts\activate

   
4. Install dependencies:

        pip install -r requirements.txt


To run the file (ensure that python3 is installed):
         
        python3 promptEngineeringExperiments.py

