from chatterbot import ChatBot
import gzip
import os


def create_chatbot(name):
    """
    Creates chatbot instance and pre-trains name
    :param name: str name of chatbot
    :return: instance of Chatterbot.Chatbot
    """

    # Instantiate chatbot
    chatbot = ChatBot(
        name=name,
        trainer='chatterbot.trainers.ListTrainer',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch'
            },
            {
                'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                'threshold': 0.5,
                'default_response': 'I am sorry, I don\'t understand right now'
            },
        ],
        filters=["chatterbot.filters.RepetitiveResponseFilter"]
    )

    # Pre-train with some simple declarations
    chatbot.train(["What is your name?", chatbot.name])
    chatbot.train(["Who are you?", chatbot.name])

    return chatbot


def process_quotes(static_file, delimiter):
    """
    Extract and Transform local file into list of conversations join by line_id<->reply_id
    :param static_file: gz file stored in app.static
    :param delimiter: delimiter used for static file
    :return: list[list[str]] of collections of conversations
    """

    with gzip.open(
            os.path.join('app', 'static', static_file), 'rt', encoding='latin-1') as gz_file:

        all_conversations = []

        for line in gz_file:
            line_array = line.split(delimiter)

            line_dict = {
                'line_id': line_array[0].strip(),
                'reply_id': line_array[4].strip(),
                'text': line_array[5].rstrip('\n').strip().lower()
            }

            if line_dict['reply_id']:

                if int(line_dict['reply_id']) + 1 == int(line_dict['line_id']):
                    all_conversations[-1].append(line_dict['text'])

            else:
                all_conversations.append([line_dict['text']])

    return all_conversations
