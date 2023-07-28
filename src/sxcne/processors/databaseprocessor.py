# Copyright (C) 2023, StarlightX.
# This source is covered under the StarlightX Public License v1.
# You should have recieved a copy of the SXPLv1 with this code.
# If not, read https://starlightx.io/licenses/sxpl.txt

import sqlite3
import json
import secrets
import string

from typing import Optional
import os

dev = False if "NODE_ENV" not in os.environ else (os.environ["NODE_ENV"] == "dev")

connection = sqlite3.connect("./test.db", check_same_thread=False)


# Key -> Token generated to make sure others cannot step on each other's chats.
def generate_random_string(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(secrets.choice(alphabet) for _ in range(length))
    return random_string


# Test connection for pytests
def connect():
     connection = sqlite3.connect("./test.db")
     try:
        connection.cursor()
        return True
     except Exception as ex:
        return False

# Delete the DB each time (data in this SQL is not important)
def initialize():

    # SQLite does not support arrays so initialize user inputs and character outputs as text as JSON.
    sql_command = "CREATE TABLE IF NOT EXISTS messages(chatid INTEGER PRIMARY KEY, conversation TEXT, additionBackstory TEXT, cacheToken TEXT)"
    connection.execute(sql_command)


# Clean up the DB to reset it, as this is just a session store.
def cleanup():

    sql_command = "DROP TABLE IF EXISTS messages"
    connection.execute(sql_command)
    
    connection.commit()



# Send conversation to the context of the chatID
def push_conversation_to_chatID(chatID: int, input: str, output: str, newEvent: Optional[str] = None):
    conversation_data = get_conversation(chatID)

    if conversation_data is not None:
        conversation, additionBackstory, cacheToken = conversation_data
    else:
        conversation = []
        cacheToken = ""
        additionBackstory = ""

    conversation.append({"input": input, "output": output})

    if newEvent is not None:
        additionBackstory.append({newEvent})

    sql_command = "INSERT OR REPLACE INTO messages (chatid, conversation, cacheToken) VALUES (?, ?, ?)"
    connection.execute(sql_command, (chatID, json.dumps(conversation), cacheToken))
    connection.commit()


def get_conversation(chatID: int):
    sql_command = "SELECT conversation, additionBackstory, cacheToken FROM messages WHERE chatid = ?"
    cursor = connection.execute(sql_command, [chatID])
    row = cursor.fetchone()

    if row:
        conversation, backstory, cacheToken = row
        input_data = json.loads(conversation)
        if backstory is not None:
            bg = json.loads(backstory)
        else:
            bg = "{}"
        return [input_data, bg, cacheToken]
    return None


# Spawn a key using a random 10 digit string
def spawnKey(chatID: int):
    purgeRowKey(chatID)
    session = generate_random_string(10)

    if dev:
        print("Added Session: ", session)


    empty_conversation = json.dumps([])
    sql_command = "INSERT INTO messages (chatid, conversation, additionBackstory, cacheToken) VALUES (?,?,?,?)"

    connection.execute(sql_command, (chatID,empty_conversation,empty_conversation,session))
    connection.commit()
    return session


def authenticateSession(chatID: int, token: str):
    if dev:
        print("CHAT: ", chatID)
        print("TOKEN: ",token)
        print("EXPECTED_TOKEN: ", get_conversation(chatID)[2])
    return (get_conversation(chatID) is not None) and (get_conversation(chatID)[2] == token)


# Clean row, called before using to keep row authentic
def purgeRowKey(chatID: int):
    sql_command = "DELETE FROM messages WHERE chatid = ?"
    connection.execute(sql_command, (chatID,))