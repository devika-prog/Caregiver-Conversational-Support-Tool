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
           
            python3 -m venv .venv 
        
    - To activate (macOS/Linux):
    
          source .venv/bin/activate
    - To activate (Windows):

            venv\Scripts\activate

   
4. Install dependencies:

        pip install -r requirements.txt


To run the file (ensure that python3 is installed):
         
        python3 promptEngineeringExperiments.py

### These are the current default values of the variables:
#chat_message: any string in the form "user: message"

      chat_message = "Student: I need help on a math problem"

#next step: string representation of suggested next steps to solving equation

      next_step = ["Subtract 2 from both sides"]

#student_hint: string representation of 'True' or 'False' (this variable holds whether or not the student has used hints)

      student_hint = 'True'

#student_accuracy: 'correct' or 'error' (this variable holds the accuracy of a previous problem-solving attempt by the student)

      student_accuracy = 'error'

#question: string representation of current equation (must be an equation involving solving for x)

#for instance, equations can be of the form: x+a=b, ax=b, ax+b=c, a(bx+c)=d, a(bx+c)+d=e, ax+b=cx, ax+b=cx+d 

      question = '6x=12'

### This is example output:
Generated message recommendation is: [Ask to self explain]  I appreciate your effort. Let's try solving the problem together. What do you think happens when we subtract 2 from both sides?

Generated message recommendation is: [Praise your child for a correct attempt]   I like how you're thinking about this problem! You're really close. Can you walk me through what you did so far?

Generated message recommendation is: [Your child has made an error]   I appreciate your effort on this problem. Let's take another look together. What was the first step you took to solve it?



