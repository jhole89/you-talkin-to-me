from chatterbot import ChatBot


def run():

    chatbot = ChatBot(
        name='Swan Ronson',
        trainer='chatterbot.trainers.ListTrainer')

    chatbot.train([
        "Hi",
        "How are you?",
        "I'm fine",
        "Me too"
    ])

    # Get a response to the input text 'How are you?'
    response = chatbot.get_response("Hi")

    print(response)


if __name__ == '__main__':
    run()
