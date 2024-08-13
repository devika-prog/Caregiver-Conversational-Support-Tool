import json
from wsgiref.simple_server import make_server
from langchain_community.llms import Ollama
from urllib.parse import parse_qs


# Set model to be LlAMA3
llm = Ollama(model="llama3")


# Starting chat message placeholder
current_chats = ['I need help solving a math problem.']

# Initialize an empty dictionary to contain lists of chat messages
sessions_dict = {}

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

#seed prompt when Python server starts
seed_string = '[I need help solving a math problem.]'
seed_prompt = prompt_context + prompt_message + seed_string + message_list_end
print('invoking seed prompt')
seed_message = llm.invoke(seed_prompt)
print('seed message is', seed_message)

def application(environ, start_response):
    headers = [
        ('Content-type', 'application/json')
    ]

    if environ['REQUEST_METHOD'] == 'OPTIONS':
        print('doing OPTIONS')
        start_response('200 OK', headers)
        return [b'']

    if environ['REQUEST_METHOD'] == 'GET':
        start_response('200 OK', headers)
        response = {'Response': 'GET not implemented, use POST'}
        return [json.dumps(response).encode('utf-8')]

    if environ['REQUEST_METHOD'] == 'POST':
        print('doing POST')
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0

        request_body = environ['wsgi.input'].read(request_body_size)
        data = json.loads(request_body.decode('utf-8'))

        # Extract data from the request
        chat_message = data.get('response', '')
        next_step = data.get('next_step', [])
        student_hint = data.get('used_hint', 'False')
        student_accuracy = data.get('accuracy', '')
        question = data.get('curr_question', '')
        sessionID = data.get('session_id', '')

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


        #create list of chat messages for each session ID
        if sessionID in sessions_dict:
            print('session ID in dictionary')
        else:
            sessions_dict[sessionID] = []

        # Store all chat messages that have been received up to that point in list current_chats
        if(not 'Typing' in chat_message):
            if(not 'NONE' in chat_message):
                sessions_dict[sessionID].append(chat_message)
                    #current_chats.append(chat_message)
                    #print('current chats are', current_chats)

        # Clear out message list 
        message_list = ['']

        # Look at all sent messages in current_chats when coming up with new responses
        chats_string = ' '.join(sessions_dict[sessionID])
        print('chats string is', chats_string)

        # Join all sent information to make complete prompt
        prompt = prompt_context + hint_prompt + acc_prompt + next_step_prompt + question_prompt + prompt_message + chats_string + message_list_end
        print('prompt is {}'.format(prompt))

        # Use the `invoke` method to generate a message based on some input prompt.
        for i in range(1):
            print('invoking prompt', i)
            messages = llm.invoke(prompt)
            #new: string splitting at # symbol
            split_string = messages.split('#')
            print('split string is', split_string)
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
                    print('new message is', new_message)
                else:
                    new_message = message
                message_list.append(new_message)

        # Sending back to Mathtutor
        data['Response'] = message_list  
        print('sent data back')
        data['curr_prompt'] = prompt
        print('message list is', message_list)
        print('handled POST')

        start_response('200 OK', headers)
        return [json.dumps(data).encode('utf-8')]

    start_response('405 Method Not Allowed', headers)
    return [b'Method Not Allowed']

#if __name__ == "__main__":
#    httpd = make_server(HOST, PORT, application)
#    print(f"Server running on {HOST}:{PORT}")
#    httpd.serve_forever()
