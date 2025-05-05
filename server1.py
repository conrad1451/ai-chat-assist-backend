from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Initialize the Gemma chat model (replace with your actual model name)
llm = ChatGoogleGenerativeAI(model_name="gemini-pro")  # Or a specific Gemma model

# Dictionary to store chat memories, keyed by session ID
chat_memories = {}

def get_or_create_memory(session_id):
    if session_id not in chat_memories:
        chat_memories[session_id] = ConversationBufferMemory()
    return chat_memories[session_id]

def chat_with_gemma(user_input, session_id):
    memory = get_or_create_memory(session_id)
    conversation = ConversationChain(
        llm=llm,
        memory=memory
    )
    response = conversation.predict(input=user_input)
    return response

# Example usage:

# Start a new chat session
session_id_1 = "user1_chat1"
user_message_1 = "Hello Gemma!"
response_1 = chat_with_gemma(user_message_1, session_id_1)
print(f"Session {session_id_1}: User - {user_message_1}, Gemma - {response_1}")

user_message_2 = "What did I just say?"
response_2 = chat_with_gemma(user_message_2, session_id_1)
print(f"Session {session_id_1}: User - {user_message_2}, Gemma - {response_2}")

# Start another independent chat session
session_id_2 = "user2_chat1"
user_message_3 = "Hi there!"
response_3 = chat_with_gemma(user_message_3, session_id_2)
print(f"Session {session_id_2}: User - {user_message_3}, Gemma - {response_3}")

user_message_4 = "How are you today?"
response_4 = chat_with_gemma(user_message_4, session_id_2)
print(f"Session {session_id_2}: User - {user_message_4}, Gemma - {response_4}")

# Check the memory of the first session
memory_session_1 = chat_memories[session_id_1]
print(f"\nMemory for Session {session_id_1}:\n{memory_session_1.load_memory_variables({})}")

# Check the memory of the second session
memory_session_2 = chat_memories[session_id_2]
print(f"\nMemory for Session {session_id_2}:\n{memory_session_2.load_memory_variables({})}")