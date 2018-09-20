#!/usr/bin/python
# coding=utf-8

from chatterbot import ChatBot
import logging

'''
This is an example showing how to train a chat bot using the
ChatterBot Corpus of conversation dialog.
'''

# Enable info level logging
logging.basicConfig(level=logging.INFO)

chatbot = ChatBot(
        'GossipBot',
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        database='./gossip_database.sqlite3',
        preprocessors=[ #预处理器
            'chatterbot.preprocessors.clean_whitespace'
        ],
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch'
            },
            {
                'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                'threshold': 0.6,
                'default_response': '正在学习中'
            }
        ],
        input_adapter="chatterbot.input.TerminalAdapter",
        output_adapter="chatterbot.output.TerminalAdapter",
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

# Start by training our bot with the ChatterBot corpus data
chatbot.train(
        'chatterbot.corpus.chinese'
)

while True:
    try:
        bot_input = chatbot.get_response(None)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break
