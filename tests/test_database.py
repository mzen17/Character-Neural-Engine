import sxcne.processors.databaseprocessor as dbp
import os

dbp.cleanup()
dbp.initialize()

os.environ["NODE_ENV"] = "dev"

def test__connection():
    dbp.connect()

# Test push function
def test__single_row():
    key = dbp.spawnKey(20)
    userinput = "Hello!"
    output = "Hi!"
    
    dbp.push_conversation_to_chatID(20, userinput, output)
    assert dbp.get_conversation(20) == [ [{ 'input': 'Hello!', 'output': 'Hi!'}], "{}", key]

def test__db_two_rows():
    key = dbp.spawnKey(50)
    userinputs = ["Hello!", "I'm doing great, thank you!"]
    outputs = ["Why, Hi! How are you doing?", "That's great to hear!"]

    dbp.push_conversation_to_chatID(50, userinputs[0], outputs[0])
    assert dbp.get_conversation(50) == [ [{'input': 'Hello!', 'output': 'Why, Hi! How are you doing?'}],"{}",  key]

    dbp.push_conversation_to_chatID(50, userinputs[1], outputs[1])
    assert dbp.get_conversation(50) == [ [{'input': 'Hello!', 'output': 'Why, Hi! How are you doing?'}, {'input': 'I\'m doing great, thank you!', 'output': 'That\'s great to hear!'}], "{}", key]

# Test Validation
def test__db_auth():
    key = dbp.spawnKey(80)
    dbp.authenticateSession(80, key)


# Test cacheing system
def test__cache():
    dbp.set_cache("Hello!", "Hi!")
    assert dbp.check_cache("Hello!") == True
    assert dbp.get_cache("Hello!") == "Hi!"