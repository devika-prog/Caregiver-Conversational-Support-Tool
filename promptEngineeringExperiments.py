'''the following is the portion of the code from our server architecture that involves
gathering different contextual information and assembling them into a prompt. 
The purpose of providing this code is for users to understand how providing different values for 
contextual information provided to the prompt
results in different generated message recommendations.'''


from langchain_community.llms import Ollama

# Set large language model to be Llama 3
llm = Ollama(model="llama3")

# list of chat messages
current_chats = ['']

prompt_context = '''You are a parent providing assistance to your middle-school child for their math homework. 
Here are some examples of good tutoring practices: 
When responding to errors, say something like:
"I appreciate your effort. Let's try solving the problem together. Can you tell me what you did first?"
"I like how hard and focused you are working on this problem. Please explain to me how you approached the first step."
"It makes me happy to see your effort. Can you show me how you started solving the problem?"

When determining what a student already knows, say something like:
"Tell me what you mean", "Talk about it some more" or "Why is that?"

When giving praise, say something like:
"Great job on solving that math problem. You persevered through solving by using a new math concept."
"I love how you tried very hard and focused on the problem!"
"You are almost there! I am proud of how you are persevering through and striving to solve the problem. Keep going!"'''

prompt_message = ''' The elements in this list are messages that have been sent in a conversation between a middle school student and their parent about a math problem (in order).
Use these messages to generate 1 to 2 sentence responses that a parent would say to their child at this point in the conversation. 
Include a short justifications in square brackets at the start of each message, such as [Ask to self explain] "Tell me what you mean", 
[Praise your child for a correct attempt] "Great job on solving that math problem.", [Your child has made an error] "I appreciate your effort."
Do not include quotation marks. Do not give away the answer. Do not directly point out errors. Generate 3 different responses, separated by the # symbol, like this: # message 1 # message 2 # message 3 #
Use the tone that the parent has been using in previous messages to generate messages with similar tone. This is the list, delimited with square brackets: [
 '''

message_list_end = ']'

# In our server, this would be extracting data from the request
#modify the values in the following 5 variables

#any string in the form "user: message"
chat_message = "Student: I need help on a math problem"

#string representation of suggested next steps to solving equation
next_step = ["Subtract 2 from both sides"]

#checks if student used hints: string representation of 'True' or 'False'
student_hint = 'True'

#checks accuracy of previous attempt: 'correct' or 'error'
student_accuracy = 'error'

#string representation of current equation
question = '6x=12'


# Initialize response components
hint_prompt = ''
next_step_prompt = ''
acc_prompt = ''
question_prompt = ''

# Process data
if next_step:
    next_step_prompt = ' Here are suggested next steps: ' + next_step[0] + ' .'
        
if student_hint == 'False':
    hint_prompt = ' Your child did not use a hint, so advise them to use one.'
else:
    hint_prompt = ' Your child did use a hint, so ask them what they understood from the hint.'

if student_accuracy == 'null':
    acc_prompt = ''
elif student_accuracy == 'error':
    acc_prompt = ' Your child made an error, so you should focus on responding to the error as described earlier.'
else:
    acc_prompt = ' Your child submitted a correct response, so praise them as described earlier.'

if question:
    question_prompt = 'This is the equation your child is working on: ' + question + 'They need to solve for x'


        
# Store all chat messages that have been received up to that point in list current_chats
if(not 'Typing' in chat_message):
    if(not 'NONE' in chat_message):
        current_chats.append(chat_message)
        # Clear out message list 
        message_list = ['']

        # Look at all sent messages in current_chats when coming up with new responses
        chats_string = ' '.join(current_chats)

        # Join all sent information to make complete prompt
        prompt = prompt_context + hint_prompt + acc_prompt + next_step_prompt + question_prompt + prompt_message + chats_string + message_list_end
        
        #Uncomment line below to view assembled prompt
        print('This is the current prompt: {}'.format(prompt))

        # Use the `invoke` method to generate a message based on some input prompt.
        messages = llm.invoke(prompt)
        #string splitting at # symbol
        split_string = messages.split('#')
        for message in split_string:
            # Find the position of the text in square brackets
            if('[' in message):
                start = message.find('[')
                end = message.find(']') + 1

                # Extract the text in square brackets
                bracket_text = message[start:end]

                # Extract the rest of the message
                rest_of_message = message[:start] + message[end:]

                # Combine the extracted text and the rest of the message
                new_message = bracket_text + " " + rest_of_message
                
            else:
                new_message = message
                message_list.append(new_message)
            print('Generated message recommendation is:', new_message)