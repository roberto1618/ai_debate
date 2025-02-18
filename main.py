'''
Main module to initialize the debate. Please see command help to understand which inputs you have to set.
'''

# Import libraries
import argparse
from dotenv import load_dotenv
import logging
import os
import yaml

from modules.debate_graph import DebateGraph

# Init logging
logging.basicConfig(level = logging.INFO)

def main():
    '''
    Main function.
    '''

    # Input parameters
    parser = argparse.ArgumentParser(description = 'Arguments to generate AI debates.')

    parser.add_argument('-n', '--debate-length', type = int, required = False, default = 16,
                        help = 'Specify the number of interventions the debate will have. By default, 16.')
    parser.add_argument('-i', '--idea1', type = str, required = True,
                        help = 'The first idea that one interlocutor must defend.')
    parser.add_argument('-j', '--idea2', type = str, required = True,
                        help = 'The second idea that the other interlocutor must defend.')
    

    args = parser.parse_args()

    n = args.debate_length
    idea1 = args.idea1
    idea2 = args.idea2

    # Load config variables
    load_dotenv()

    with open('./config.yml', 'r') as f:
        config = yaml.safe_load(f)

    system_prompt_interlocutor = config['prompts']['system_prompt_interlocutor']
    system_prompt_supervisor = config['prompts']['system_prompt_supervisor']

    AZURE_DEPLOYMENT_LLM_MODEL = os.getenv('AZURE_DEPLOYMENT_LLM_MODEL')
    OPENAI_API_VERSION = os.getenv('OPENAI_API_VERSION')

    # Init Debate class
    debate_graph = DebateGraph(deployment_name = AZURE_DEPLOYMENT_LLM_MODEL,
                               system_prompt_interlocutor = system_prompt_interlocutor,
                               system_prompt_supervisor = system_prompt_supervisor,
                               idea1 = idea1,
                               idea2 = idea2,
                               n = n)
    
    # Init debate
    debate_graph.init_debate()

if __name__ == '__main__':
    main()