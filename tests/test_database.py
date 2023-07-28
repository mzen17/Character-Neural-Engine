import sxcne.processors.databaseprocessor as dbp

dbp.cleanup()
dbp.initialize()

def test__connection():
    dbp.connect()

# Test push function
def test__single_row():
    key = dbp.spawnKey(20)
    userinput = "Hello!"
    output = "Hi!"
    
    dbp.push_conversation_to_chatID(20, userinput, output)
    assert dbp.get_conversation(20) == [ [{ 'input': 'Hello!', 'output': 'Hi!'}], "{}", key]


def test_db_multirow():
    key = dbp.spawnKey(50)
    userinputs = ["Hello!", "I'm doing great, thank you!"]
    outputs = ["Why, Hi! How are you doing?", "That's great to hear!"]

    dbp.push_conversation_to_chatID(50, userinputs[0], outputs[0])
    assert dbp.get_conversation(50) == [ [{'input': 'Hello!', 'output': 'Why, Hi! How are you doing?'}],"{}",  key]

    dbp.push_conversation_to_chatID(50, userinputs[1], outputs[1])
    assert dbp.get_conversation(50) == [ [{'input': 'Hello!', 'output': 'Why, Hi! How are you doing?'}, {'input': 'I\'m doing great, thank you!', 'output': 'That\'s great to hear!'}], "{}", key]

# Test Cache Validation
def test__db_auth():
    key = dbp.spawnKey(80)
    dbp.authenticateSession(80, key)
