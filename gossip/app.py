from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

# english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")

# english_bot.set_trainer(ChatterBotCorpusTrainer)
# english_bot.train("chatterbot.corpus.english")


chatbot = ChatBot(
        'GossipBot',
        storage_adapter="chatterbot.storage.SQLStorageAdapter",       
        preprocessors=[ #预处理器
            'chatterbot.preprocessors.clean_whitespace'
        ],
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch'
            }
            # ,
            # {
            #     'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            #     'threshold': 0.6,
            #     'default_response': '小智正在学习中'
            # }
        ],
        #input_adapter="chatterbot.input.TerminalAdapter",
        #output_adapter="chatterbot.output.TerminalAdapter",
        output_adapter="chatterbot.output.OutputAdapter",
        output_format="text"
        #trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)
# Start by training our bot with the ChatterBot corpus data
chatbot.set_trainer(ChatterBotCorpusTrainer)
chatbot.train('chatterbot.corpus.chinese')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))


if __name__ == "__main__":
    app.run()#host='0.0.0.0'
