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
                'text': line_array[5].rstrip('\n').strip()
            }

            if line_dict['reply_id']:
                if int(line_dict['reply_id']) - 1 == int(line_dict['line_id']):
                    all_conversations[-1].append(line_dict['line_id'] + '---' + line_dict['text'])
            else:
                all_conversations.append([line_dict['text']])

        return all_conversations


def run():

    chatbot = ChatBot(
        name='Swan Ronson',
        trainer='chatterbot.trainers.ListTrainer')

    training_dialog = _preprocess()

    print(training_dialog)

    chatbot.train([
        "Hi",
        "How are you?",
        "I'm fine",
        "Me too"
    ])

    # Get a response to the input text 'How are you?'
    response = chatbot.get_response("I'm fine")

    print(response)


if __name__ == '__main__':
    run()
