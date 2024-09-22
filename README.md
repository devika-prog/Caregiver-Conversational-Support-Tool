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

Install required dependencies before running:
1. Download [Ollama]([docs/CONTRIBUTING.md](https://ollama.com/download/mac))
2. Create a virtual environment (only necesssary if prompted)
   
    - To create:
    
          python -m venv .venv
    - To activate:
    
          source .venv/bin/activate
   
3. Install the langchain dependencies:

        pip install langchain-community

