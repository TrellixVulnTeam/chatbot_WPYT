# -*- coding: UTF-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals



import argparse
import logging
import warnings

from rasa_core.actions import Action
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.events import SlotSet
from rasa_core.events import Restarted
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy


logger = logging.getLogger(__name__)


"""
nul train param
"""
nlu_training_data = "data/nlu_data.json"
nlu_model_config = "nlu_model_config.json"
nlu_project_name = "bocbot"
nlu_fixed_model_name = "nlu_bocbot"
nlu_model_save_dir = "models/"
nlu_interpreter = nlu_model_save_dir + nlu_project_name + '/' + nlu_fixed_model_name

"""
dialogue train param
"""
dm_domain_file = "dm_domain.yml";
dm_training_data = "data/dm_story.md";
dm_model_path = "models/dialogue"

'''自己改写训练策略
class BocdcBotPolicy(KerasPolicy):
    def model_architecture(self, num_features, num_actions, max_history_len):
        """Build a Keras model and return a compiled model."""
        from keras.layers import LSTM, Activation, Masking, Dense
        from keras.models import Sequential

        n_hidden = 32  # size of hidden layer in LSTM
        # Build Model
        batch_shape = (None, max_history_len, num_features)

        model = Sequential()
        model.add(Masking(-1, batch_input_shape=batch_shape))
        model.add(LSTM(n_hidden, batch_input_shape=batch_shape))
        model.add(Dense(input_dim=n_hidden, output_dim=num_actions))
        model.add(Activation("softmax"))

        model.compile(loss="categorical_crossentropy",
                      optimizer="adam",
                      metrics=["accuracy"])

        logger.debug(model.summary())
        return model
'''

def train_dialogue():
    '''
    training dm model

    Returns:

    '''
    agent = Agent(dm_domain_file, policies=[MemoizationPolicy(), KerasPolicy()])

    agent.train(
        dm_training_data,
        max_history=3,
        epochs=400,
        batch_size=100,
        augmentation_factor=50,
        validation_split=0.2
    )

    agent.persist(dm_model_path)
    return agent


def train_nlu():
    '''
    training nlu model

    Returns: model dir

    '''
    from rasa_nlu.converters import load_data
    from rasa_nlu.config import RasaNLUConfig
    from rasa_nlu.model import Trainer

    training_data = load_data(nlu_training_data)
    trainer = Trainer(RasaNLUConfig(nlu_model_config))
    trainer.train(training_data)
    model_directory = trainer.persist(nlu_model_save_dir, project_name=nlu_project_name, fixed_model_name=nlu_fixed_model_name)

    return model_directory


def online_train():
    '''

    :return:
    '''
    input_channel = ConsoleInputChannel()
    interpreter = RasaNLUInterpreter(nlu_interpreter)
    agent = Agent(dm_domain_file,
                  policies=[MemoizationPolicy(), KerasPolicy()],
                  interpreter=interpreter)

    agent.train_online(dm_training_data,
                       input_channel=input_channel,
                       max_history=2,
                       batch_size=50,
                       epochs=200,
                       max_training_samples=300)

    return agent

def visualize_dialogue():
    agent = Agent(dm_domain_file,
                  policies=[MemoizationPolicy(), KerasPolicy()])

    agent.visualize(dm_training_data,
                    output_file="graph.png", max_history=2)

    return agent
    # domain = TemplateDomain.load(dm_domain_file)
    # stories = StoryFileReader.read_from_file(dm_training_data, domain)

    # visualize_stories(stories, "graph.png")

def run(serve_forever=True):
    '''
    start to run bot

    Args:
        serve_forever:

    Returns:

    '''
    agent = Agent.load(dm_model_path, interpreter=RasaNLUInterpreter(nlu_interpreter))

    if serve_forever:
        agent.handle_channel(ConsoleInputChannel())
    return agent


if __name__ == "__main__":
    logging.basicConfig(level="INFO")

    parser = argparse.ArgumentParser(description="starts the bot")

    parser.add_argument(
        "task",
        choices=["train-nlu", "train-dialogue", "run", "online-train", "visualize-dialogue"],
        help="what the bot should do - e.g. run or train?")
    task = parser.parse_args().task

    # decide what to do based on first parameter of the script
    if task == "train-nlu":
        train_nlu()
    elif task == "train-dialogue":
        train_dialogue()
    elif task == "run":
        run()
    elif task == "online-train":
        online_train()
    elif task == "visualize-dialogue":
        visualize_dialogue()
    else:
        warnings.warn("Need to pass either 'train-nlu', 'train-dialogue', "
                      "'run', or 'visualize-dialogue', 'online-train' to use the script.")
        exit(1)
