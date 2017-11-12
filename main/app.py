# -*- coding: utf-8 -*-
from chatterbot import ChatBot
import gzip
import os


def _preprocess():
    with gzip.open(
            os.path.join('main', 'resources', 'moviequotes.scripts.txt.gz'), 'rt', encoding='latin-1') as gz_file:

        all_conversations = []

        for line in gz_file:
            line_array = line.split('+++$+++')

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


def run(train):

    chatbot = ChatBot(
        name='Arnold Schwarzenatter',
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

    if train:

        training_dialog = _preprocess()

        for conversation in training_dialog:
            if len(conversation) > 7:
                chatbot.train(conversation)

    response = chatbot.get_response("hi")

    print(response)


if __name__ == '__main__':
    run(train=False)
