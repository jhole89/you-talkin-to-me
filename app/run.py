# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, Response
from app.controllers import process_quotes, create_chatbot
from random import shuffle
import logging


app = Flask(__name__)
chatbot = create_chatbot(name='Arnold Schwartzenatter')


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/question/<string:query>')
def get_raw_response(query):
    return str(chatbot.get_response(query))


@app.route('/admin/retrain', methods=['POST'])
def retrain_corpus():

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
