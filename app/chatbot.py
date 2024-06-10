# chatbot.py
from app.library import *

def process_chat_message(message, user_id):
    # Implement chatbot logic here
    client = current_app.client
    db = current_app.db

    thread_id = get_thread_id(user_id)
    status = run_gpt(thread_id,message)

    if status =='completed':
        reply = write_database(thread_id)

    else:
        db.collection('mysite').add({'Message':message, 'Role':'user', 'Thread ID':thread_id,'Timestamp':datetime.now()})
        reply = 'There has been some issue with ChatGPT'
        print(thread_id)

    return reply






def get_thread_id(user_id):
    db = current_app.db
    client = current_app.client

    docs = db.collection('threads').stream()
    retrieved_data = [doc.to_dict() for doc in docs]
    df_retrieved = pd.DataFrame(retrieved_data)

    thread_id = df_retrieved[df_retrieved['user_id']==user_id]['thread ID']

    try:
        thread_id = thread_id.iloc[0]
    except IndexError:
        thread = client.beta.threads.create()
        thread_id = thread.id
        db.collection('threads').add({'thread ID':thread_id, 'user_id':user_id, 'Timestamp':datetime.now()})

    return thread_id




def extract(messages_object):
    thread_ids = []
    roles = []
    messages = []
    timestamps = []

    for message in messages_object.data:
        # Extract thread ID and add it to the list
        thread_ids.append(message.thread_id)

        # Extract the role and add it to the list
        roles.append(message.role)

        # Extract the message text and add it to the list
        message_text = message.content[0].text.value if message.content else None
        messages.append(message_text)

        # Convert timestamp to a human-readable format including day, month, year, hour, minute, and second
        readable_timestamp = datetime.fromtimestamp(message.created_at).strftime('%d %b %Y %H:%M:%S')
        timestamps.append(readable_timestamp)

    df = pd.DataFrame({
        'Thread ID': thread_ids,
        'Role': roles,
        'Message': messages,
        'Timestamp': timestamps
    })

    # Convert 'Timestamp' column to datetime for sorting
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Sort the DataFrame by 'Timestamp' in ascending order
    df = df.sort_values(by='Timestamp')
    df = df.reset_index(drop=True)

    return df




def run_gpt(thread_id, message):
    client = current_app.client

    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )
    
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id= current_app.config['ASSISTANT_ID']
    )
    print(run.id)
    while run.status not in ['completed', 'failed']:
        time.sleep(1)  # Wait for 2 seconds before checking again
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        
    return run.status



def write_database(thread_id):
    client = current_app.client
    db = current_app.db

    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    df = extract(messages)

    records = df.iloc[-2:,:].to_dict(orient='records')

    for record in records:
        db.collection('mysite').add(record)
    
    reply = df.iloc[-1,:]['Message']

    return reply