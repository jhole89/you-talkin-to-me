# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, Response
from app.controllers import process_quotes, create_chatbot
from random import shuffle
import logging


app = Flask(__name__)
chatbot = create_chatbot(name='Arnold Schwartzenatter')


@app.route('/')
def home():
    """
    API endpoint for home /
    :return: rendered index.html page
    """
    return render_template("index.html")


@app.route('/question/<string:query>')
def get_response(query):
    """
    API endpoint for /question/
    :param query: string query to send to chatbot
    :return: Flask.Response object wrapping result from chatbot with given query
    """
    return Response(str(chatbot.get_response(query)), status=200)


@app.route('/admin/retrain', methods=['POST'])
def retrain_corpus():
    """
    API endpoint for /admin/retrain. Should take a json object of body {"conversation_length": int, "stop_short": int}
    :return: Flask.Response object
    """

    all_conversations = process_quotes(
        static_file='moviequotes.scripts.txt.gz',
        delimiter='+++$+++')

    retrain_settings = request.get_json()
    max_conversations = retrain_settings.get('stop_short')
    shuffle(all_conversations)

    for conv_id, conversation in enumerate(all_conversations[:max_conversations]):

        if len(conversation) > retrain_settings.get('conversation_length'):

            chatbot.train(conversation)

            app.logger.info(
                'Training: {0:.2f}% complete'.format(
                    100*float(conv_id)/float(max_conversations)
                )
            )

    return Response("Retrained with parameters: {}".format(retrain_settings), status=200)


if __name__ == '__main__':
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

    app.run()
