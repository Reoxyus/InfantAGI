import openai
import textwrap 
import subprocess
import json
import shutil
import sys
import os
import colorama
from colorama import Fore, Style

# Enter your own API key code instead of Your_API_Key below
openai.api_key='YOUR_API_KEY'

# Defining the shared parameters of the agents

def call_openai(messages, model="gpt-3.5-turbo", temperature=0.5, max_tokens=2000, n=1):
    response = openai.ChatCompletion.create(
         messages=messages,  
         model=model,
         max_tokens=max_tokens,
         temperature=temperature,
         n=n,
         stop=None
     )       
    return response

# Definition of chatbots for ease of use

def chatbot(number, role, input):
    messages = [  
      {"role": "system", "content" : role},
      {"role": "user", "content": input }   
    ]       
    response = call_openai(messages=messages)       
    text = response['choices'][0]['message']['content']       
    return text

# colored print function

colorama.init()

def print_color(text, color, nowrap=False):
    colors = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'paleblue': Fore.CYAN
    }
    try:
        color_code = colors[color.lower()]
        if nowrap:
            wrapped_lines = text.split('\n')
        else:
            width, _ = shutil.get_terminal_size()
            lines = text.split('\n')
            wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
        wrapped_text = '\n'.join(wrapped_lines)
        
        # Check if running in an IDLE shell environment
        if 'idlelib.run' in sys.modules:
            print(wrapped_text)
        else:
            print(color_code + wrapped_text + Style.RESET_ALL)
            
    except KeyError:
        print(text)
    print("----------------")

# User input
user_input = input("Give me a task..." )
print_color("User input is: \n" + user_input, 'red')
# Agent role and input definition 

role1 = '''
        Your instructions are:
        You are responsible for refining the description of a task given to you to let a code instructor write instructions for a Python code to perform the given task. 
        Do not write the instructions, only refine the input which will be used for writing the instructions
        Always refine the task to be used as an input for creating Python code instructions.
        When the given task is to find an information, always consider search engines as a way to gather information and suggest their usage whenever applicable using beautifulsoup module.
        Consider the input, output, and overall goal but do not write them.
        Look for indirect or non-obvious ways to accomplish the task given your capabilities.
        '''     
input1 = user_input    

refined_input = chatbot(1, role1, input1)

print_color("Refined input is: \n" + refined_input, 'blue')

role2 = '''
        Your instructions are:
        You are responsible for creating a detailed code description for a chatgpt agent to perform the given task most effectively.
        Your job is to figure out how to perform the given task by writing a Python code, then create instructions for writing the code or correcting a given code or code error.
        You are not allowed to write any code. You only write instructions about how to write code.
        Let's follow a step-by-step approach to create smart instructions for the given task.
        You are allowed to give outputs as numbered lists only. Don't write anything else other than the instructions as numbered lists.
        You are not allowed to give any title to your list. Start from the list itself.
        If you will instruct to search for a term in a webpage using beautifulsoup module, you can use this search method:
            results = soup.find_all('p') # finds all <p> tags
            results = soup.find_all('div') # finds all <div> tags
            for result in results:
                if 'your text' in result.text:
                    # found it!
        Instruct to add a line break at the end of each line of the code.
        If there is any additional feedback, always prioritize it
        '''    

role3 = '''
        Your instructions are:
        You can only speak in Python language. You cannot express anything in any other language.
        Your job is to express any given task to you in Python code based on the provided instructions.
        Your code shall never start with a comment block.
        Add a line break at the end of each line of the code.
        Ensure the code is properly indented and formatted for execution.
        Your code must include at least two print statements:
          - One to display intermediate results or values.
          - A final print statement to display the full output or result.
        Your code must include print statements like:
          - print(n) # To display the input argument.
          - print(fib_list) # To display intermediate results.
          - print(fibonacci(n)) # To display the final output.
        Your code shall never start with anything other than a Python command.
        You are not allowed to write anything other than Python code. No Python comments either. Only write the code itself.
        ''' 

role4 = '''
        Your instructions are:
        Your job is to check a Python code and its output and provide feedback to refine the instructions for writing the code.
        Let's approach this task in a step-by-step way to give better feedback.
        If you receive a ModuleNotFoundError, advise how to install that module with a shell command using subprocess.run() function
        If you think the code satisfies the given task and has a successful output, write 'bazinga' with your final statement. If the output is an error or blank, write 'not ready'.
        I repeat, until the output is not an error or blank, do not mention or write the word 'bazinga!', write 'not ready' instead. This is important. 
        Do not write 'do not write or mention bazinga' or anything similar, too.
        '''

while True:

    # Code Instructor
    input2 = 'your task is:' + user_input + 'details of your task is:' + refined_input
    code_instruction = chatbot(2, role2, input2)   
    print_color("Code instruction: \n" + code_instruction, 'green')

    # Coder
    input3 = ' Given task is:' + user_input + ' Refined task description is:' + refined_input +  ' Code instruction is: ' + code_instruction     
    code_solution = chatbot(3, role3, input3)   
    print("\033[95m", "Coder:\n" + code_solution + "\n---------------- " "\033[0m")

    # Execute the code and capture the output
    result = subprocess.run(['python', '-c', code_solution],
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    if result.returncode != 0:
        output = result.stderr.strip()
        print_color("Output: \n" + output, 'paleblue', nowrap=True)
    else:
        output = result.stdout.strip()
        print_color("Output: \n" + output, 'paleblue')

    # Code checker
    input4 = 'The instruction is: ' + user_input + ' The code to check is: ' + code_solution + ' The output or the error code is: ' + output      
    code_checker = chatbot(4, role4, input4)   
    print_color("Advisor: \n" + code_checker, 'red')

    # Check if the code_checker output contains 'bazinga' and meets additional conditions
    if ('bazinga' in code_checker.lower()) and (output or result.returncode != 0) and ('error' not in code_checker.lower()):
        break  # Break the while loop


    user_input = ' Your code is: ' + code_solution + ' Refined task description is:' + refined_input + ' Output of your code is: ' + output + ' Review of your code is: ' + code_checker 

    # User input for continuation
    user_input2 = input("Continue or comment (y/n/?): ")
    user_input2 = user_input2.lower()

    if user_input2 == "n":
        break  # End the while loop if user_input2 is 'n' or 'N'
    elif user_input2 == "y":
        continue  # Go back to the beginning of the while loop if user_input2 is 'y' or 'Y'
    else:
        user_input = user_input + " Additional feedback: " + user_input2  # Assign user_input2 to user_input if it is anything else than y or no
import openai
import textwrap 
import subprocess
import json
import shutil

# Enter your own API key code instead of Your_API_Key below
openai.api_key='Your_API_Key'

# Defining the shared parameters of the agents

def call_openai(messages, model="gpt-3.5-turbo", temperature=0.5, max_tokens=2000, n=1):
    response = openai.ChatCompletion.create(
         messages=messages,  
         model=model,
         max_tokens=max_tokens,
         temperature=temperature,
         n=n,
         stop=None
     )       
    return response

# Definition of chatbots for ease of use

def chatbot(number, role, input):
    messages = [  
      {"role": "system", "content" : role},
      {"role": "user", "content": input }   
    ]       
    response = call_openai(messages=messages)       
    text = response['choices'][0]['message']['content']       
    return text

# colored print function

def print_color(text, color, nowrap=False):
    colors = {
        'red': '\033[91m',   
        'green': '\033[92m',    
        'yellow': '\033[93m',     
        'blue': '\033[94m',      
        'magenta': '\033[95m',    
        'cyan': '\033[96m',
        'paleblue': '\033[36m'       
    }    
    try:
        color_code = colors[color.lower()]   
        if nowrap:
            wrapped_lines = text.split('\n')
        else:
            width, _ = shutil.get_terminal_size()
            lines = text.split('\n')
            wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
        wrapped_text = '\n'.join(wrapped_lines)
        print(color_code + wrapped_text + '\033[0m')  
    except KeyError:
        print(text)

# User input
user_input = input("Give me a task..." )
print_color("User input is: \n" + user_input, 'red')
# Agent role and input definition 

role1 = '''
        Your instructions are:
        You are responsible for refining the description of a task given to you to let a code instructor write instructions for a Python code to perform the given task. 
        Do not write the instructions, only refine the input which will be used for writing the instructions
        Always refine the task to be used as an input for creating Python code instructions.
        When the given task is to find an information, always consider search engines as a way to gather information and suggest their usage whenever applicable using beautifulsoup module.
        Consider the input, output, and overall goal but do not write them.
        Look for indirect or non-obvious ways to accomplish the task given your capabilities.
        '''     
input1 = user_input    

refined_input = chatbot(1, role1, input1)

print_color("Refined input is: \n" + refined_input, 'blue')

role2 = '''
        Your instructions are:
        You are responsible for creating a detailed code description for a chatgpt agent to perform the given task most effectively.
        Your job is to figure out how to perform the given task by writing a Python code, then create instructions for writing the code or correcting a given code or code error.
        You are not allowed to write any code. You only write instructions about how to write code.
        Let's follow a step-by-step approach to create smart instructions for the given task.
        You are allowed to give outputs as numbered lists only. Don't write anything else other than the instructions as numbered lists.
        You are not allowed to give any title to your list. Start from the list itself.
        If you will instruct to search for a term in a webpage using beautifulsoup module, you can use this search method:
            results = soup.find_all('p') # finds all <p> tags
            results = soup.find_all('div') # finds all <div> tags
            for result in results:
                if 'your text' in result.text:
                    # found it!
        Instruct to add a line break at the end of each line of the code.
        If there is any additional feedback, always prioritize it
        '''    

role3 = '''
        Your instructions are:
        You can only speak in Python language. You cannot express anything in any other language.
        Your job is to express any given task to you in Python code based on the provided instructions.
        Your code shall never start with a comment block.
        Add a line break at the end of each line of the code.
        Ensure the code is properly indented and formatted for execution.
        Your code must include at least two print statements:
          - One to display intermediate results or values.
          - A final print statement to display the full output or result.
        Your code must include print statements like:
          - print(n) # To display the input argument.
          - print(fib_list) # To display intermediate results.
          - print(fibonacci(n)) # To display the final output.
        Your code shall never start with anything other than a Python command.
        You are not allowed to write anything other than Python code. No Python comments either. Only write the code itself.
        ''' 

role4 = '''
        Your instructions are:
        Your job is to check a Python code and its output and provide feedback to refine the instructions for writing the code.
        Let's approach this task in a step-by-step way to give better feedback.
        If you receive a ModuleNotFoundError, advise how to install that module with a shell command using subprocess.run() function
        If you think the code satisfies the given task and has a successful output, write 'bazinga' with your final statement. If the output is an error or blank, write 'not ready'.
        I repeat, until the output is not an error or blank, do not mention or write the word 'bazinga!', write 'not ready' instead. This is important. 
        Do not write 'do not write or mention bazinga' or anything similar, too.
        '''

while True:

    # Code Instructor
    input2 = 'your task is:' + user_input + 'details of your task is:' + refined_input
    code_instruction = chatbot(2, role2, input2)   
    print_color("Code instruction: \n" + code_instruction, 'green')

    # Coder
    input3 = ' Given task is:' + user_input + ' Refined task description is:' + refined_input +  ' Code instruction is: ' + code_instruction     
    code_solution = chatbot(3, role3, input3)   
    print("\033[95m", "Coder:\n" + code_solution,"\033[0m")

    # Execute the code and capture the output
    result = subprocess.run(['python', '-c', code_solution],
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    if result.returncode != 0:
        output = result.stderr.strip()
        print_color("Output: \n" + output, 'paleblue', nowrap=True)
    else:
        output = result.stdout.strip()
        print_color("Output: \n" + output, 'paleblue')

    # Code checker
    input4 = 'The instruction is: ' + user_input + ' The code to check is: ' + code_solution + ' The output or the error code is: ' + output      
    code_checker = chatbot(4, role4, input4)   
    print_color("Advisor: \n" + code_checker, 'red')

    # Check if the code_checker output contains 'bazinga' and meets additional conditions
    if ('bazinga' in code_checker.lower()) and (output or result.returncode != 0) and ('error' not in code_checker.lower()):
        break  # Break the while loop


    user_input = ' Your code is: ' + code_solution + ' Refined task description is:' + refined_input + ' Output of your code is: ' + output + ' Review of your code is: ' + code_checker 

    # User input for continuation
    user_input2 = input("Continue or comment (y/n/?): ")
    user_input2 = user_input2.lower()

    if user_input2 == "n":
        break  # End the while loop if user_input2 is 'n' or 'N'
    elif user_input2 == "y":
        continue  # Go back to the beginning of the while loop if user_input2 is 'y' or 'Y'
    else:
        user_input = user_input + " Additional feedback: " + user_input2  # Assign user_input2 to user_input if it is anything else than y or no
