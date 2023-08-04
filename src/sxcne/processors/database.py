# Copyright (C) 2023, StarlightX.
# This source is covered under the StarlightX Public License v1.
# You should have recieved a copy of the SXPLv1 with this code.
# If not, read https://starlightx.io/licenses/sxpl.txt

import json
import secrets
import string
from typing import Optional
import os
import psycopg as psycopg

dev = False if "NODE_ENV" not in os.environ else (os.environ["NODE_ENV"] == "dev")

# Check if environment variables are set
if ("DB_NAME" not in os.environ) or ("DB_USER" not in os.environ) or ("DB_PASS" not in os.environ) or ("DB_HOST" not in os.environ) or ("DB_PORT" not in os.environ):
    print("CRITICAL ERROR: DATABASE CONFIGS NOT SET!! APP WILL NOT WORK!")

    # Print which one was not set
    if "DB_NAME" not in os.environ:
        print("DB_NAME not set!")
    if "DB_USER" not in os.environ:
        print("DB_USER not set!")
    if "DB_PASS" not in os.environ:
        print("DB_PASSWORD not set!")
    if "DB_HOST" not in os.environ:
        print("DB_HOST not set!")
    if "DB_PORT" not in os.environ:
        print("DB_PORT not set!")
    exit

# Database configs
db_name = os.environ["DB_NAME"] if "DB_NAME" in os.environ else "postgres"
db_user = os.environ["DB_USER"] if "DB_USER" in os.environ else "postgres"
db_pass = os.environ["DB_PASS"] if "DB_PASS" in os.environ else "postgres"
db_host = os.environ["DB_HOST"] if "DB_HOST" in os.environ else "localhost"
db_port = os.environ["DB_PORT"] if "DB_PORT" in os.environ else 5432

# Key -> Token generated to make sure others cannot step on each other's chats.
def generate_random_string(length):
    alphabet = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(alphabet) for _ in range(length))
    return random_string

# Test connection for pytests
def connect():
    try:
        connection = psycopg.connect(
            dbname=db_name,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
        )
        connection.cursor()
        return True
    except Exception as ex:
        return False


def initialize():
    connection = psycopg.connect(
        dbname=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
    )
    cursor = connection.cursor()
    sql_command = "CREATE TABLE IF NOT EXISTS messages(chatid SERIAL PRIMARY KEY, conversation JSONB[], additionBackstory TEXT, cacheToken TEXT)"
    cursor.execute(sql_command)

    sql_command = "CREATE TABLE IF NOT EXISTS cache(id serial PRIMARY KEY, input vector(384), output TEXT)"
    cursor.execute(sql_command)

    connection.commit()


def cleanup():
    connection = psycopg.connect(
        dbname=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
    )
    cursor = connection.cursor()

    sql_command = "DELETE from messages"
    cursor.execute(sql_command)

    connection.commit()


def push_conversation_to_chatID(chatID: int, input_str: str, output_str: str, newEvent: Optional[str] = None):
    connection = psycopg.connect(
        dbname=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
    )
    conversation_data = get_conversation(chatID)

    if conversation_data is not None:
        conversation, additionBackstory, cacheToken = conversation_data
        print(conversation)
    else:
        conversation = []
        cacheToken = ""
        additionBackstory = "{}"

    conversation.append({"input": input_str, "output": output_str})

    if newEvent is not None:
        additionBackstory.append(newEvent)

    for i in range(len(conversation)):
        conversation[i] = json.dumps(conversation[i])

    sql_command = "INSERT INTO messages (chatid, conversation, cacheToken) VALUES (%s, %s, %s) ON CONFLICT (chatid) DO UPDATE SET conversation = %s, cacheToken = %s"
    
    print(type(conversation))

    connection.execute(sql_command, (chatID, conversation, cacheToken, conversation, cacheToken))
    connection.commit()


# Search by chatID (index)
def get_conversation(chatID: int):
    connection = psycopg.connect(
        dbname=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
    )
    cursor = connection.cursor()

    sql_command = "SELECT conversation, additionBackstory, cacheToken FROM messages WHERE chatid = %s"
    cursor.execute(sql_command, [chatID]) 

    row = cursor.fetchone()
    cursor.close()   
    connection.close() 

    if row:
        conversation, backstory, cacheToken = row
        input_data = conversation
        if backstory is not None:
            bg = backstory
        else:
            bg = "{}"
        return [input_data, bg, cacheToken]
    return None


def spawnKey(chatID: int):
    connection = psycopg.connect(
        dbname=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
    )
    cursor = connection.cursor()

    purgeRowKey(chatID)
    session = generate_random_string(10)

    if dev:
        print("Added Session: ", session)

    sql_command = "INSERT INTO messages (chatid, conversation, additionBackstory, cacheToken) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql_command, (chatID, [], "{}", session))

    connection.commit()
    return session


def authenticateSession(chatID: int, token: str):
    if dev:
        print("CHAT: ", chatID)
        print("TOKEN: ", token)
        print("EXPECTED_TOKEN: ", get_conversation(chatID)[2])
    return (get_conversation(chatID) is not None) and (get_conversation(chatID)[2] == token)


def purgeRowKey(chatID: int):
    connection = psycopg.connect(
        dbname=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
    )
    cursor = connection.cursor()

    sql_command = "DELETE FROM messages WHERE chatid = %s"
    cursor.execute(sql_command, (chatID,))

    connection.commit()

## Cache server commands
def get_cache(input_vector, similarity_threshold=0.5):
    connection = psycopg.connect(
        dbname=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
    )

    cursor = connection.cursor()

    # Perform a similarity search using the pgvector operator <->
    sql_command = """
        SELECT output
        FROM cache
        WHERE input <-> %s < %s
        ORDER BY input <-> %s
        LIMIT 1;
        """

    vec = "[" + ",".join(map(str, input_vector)) + "]"

    cursor.execute(sql_command, (vec, similarity_threshold, vec))
    row = cursor.fetchone()
    if row:
        return row[0]
    return None


def set_cache(input_str, output_str: str):
    connection = psycopg.connect(
        dbname=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
    )
    cursor = connection.cursor()

    if(get_cache(input_str) != None):
        sql_command = "DELETE FROM cache WHERE input = %s"

    sql_command = "INSERT INTO cache (input, output) VALUES (%s, %s)"
    cursor.execute(sql_command, (input_str, output_str))

    connection.commit()
