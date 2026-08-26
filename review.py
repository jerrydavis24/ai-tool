import sys ##FOR sys.argv
import anthropic

filename = sys.argv[1]##sys.argv is how a python script reads what you typed after its name on the command line
##When you run python review.py main.py, sys.argv[1] holds the string "main.py"

client = anthropic.Anthropic()##an instance of the anthropic class
##the anthropic class is like a blueprint for a connection to anthropics API

tf= True
while tf:

##the below with line of code is what opens the file that is passed as the second argument in the command line
##remember we run this code with python review.py /path/to/file
    try:
        with open(filename) as f:
            code_text = f.read()
    except:
        print("A file wasn't opened to be read!")
        tf=False
        continue


    try:
##this is the block of code that generates the ai generated code review
        message = client.messages.create(##calling the create method on client.messages, this is what actually sends a request to the API and gets a response
            model="claude-opus-5",
            max_tokens=4096,##this caps how long the response is allowed to be 4096 is a good number, 300 is good for debugging    
    ##building a chat message that says to reveiw this code
    ##recall that we placed the python code in a variable named code_text
    ##this is in a list because that is the format the api expects
            messages=[{
                "role": "user",
            "content": f"Review this Python code and list concrete issues:\n\n{code_text}"
            }]
        )
    except:
        print("Something went wrong reaching the AP - check the connection or API key.")
        tf= False
        continue

##print(message)

##this is the part that actually pulls the readable
##text out of the response and prints it to the terminal
##make sure that we are only printing text to the user
    for block in message.content:
        if block.type == "text":
            print(block.text)

    print("enter 1 for yes or 0 for no")
    try:
        choice= int(input("Would you like to ask another question? "))
        if choice == 1:
            tf= True
            filename=str(input("Enter the path to the file that you would like to be reviewed"))
        else:
            tf= False
    except:
        print("the input provided was invalid")
        tf= False
