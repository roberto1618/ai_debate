'''
This module contains the main class to create the Debate Graph.
'''

# Import libraries
from fpdf import FPDF
from datetime import datetime
import pyttsx3
from typing import Literal
import logging

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage, RemoveMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END

from modules.state import State

class DebateGraph:
    '''
    Main Debate class.
    '''

    def __init__(self, deployment_name, system_prompt_interlocutor, system_prompt_supervisor, idea1, idea2, n):
        '''
        Init function.

        :param deployment_name: The deployment LLM name.
        :type deployment_name: string
        :param system_prompt_interlocutor: Prompt that interlocutors must follow.
        :type system_prompt_interlocutor: string
        :param system_prompt_supervisor: Prompt that supervisor must follow.
        :type system_prompt_supervisor: string
        :param idea1: First idea to defend in the debate.
        :type idea1: string
        :param idea2: Second idea to defend in the debate.
        :type idea2: string
        :param n: Debate length.
        :type n: integer
        '''

        # Init variables
        self.llm = AzureChatOpenAI(deployment_name = deployment_name,
                        model = deployment_name)
        self.system_prompt_interlocutor = system_prompt_interlocutor
        self.system_prompt_supervisor = system_prompt_supervisor
        self.idea1 = idea1
        self.idea2 = idea2
        self.n = n
        
    def interlocutor1(self, state: State):
        '''
        First interlocutor node.

        :param state: Graph State.
        :type state: StateGraph class
        '''

        logging.info('---INTERLOCUTOR 1---')
        # Set messages and metadata variable
        messages = state['messages']
        response_metadata = {'interlocutor': 'Interlocutor1'}

        # Change the message type because AIs must alternate the messages type order
        for i, m in enumerate(messages):
            if isinstance(m, HumanMessage):
                messages[i] = AIMessage(content = m.content)
            if isinstance(m, AIMessage):
                messages[i] = HumanMessage(content = m.content)

        # Get summary if it is avaliable
        summary = state.get('summary', '')

        if summary:
            system_message = f'{self.system_prompt_interlocutor.format(idea = state['idea1'])}\n\nResumen de lo que habéis hablado anteriormente en el debate: {summary}'
        else:
            system_message = self.system_prompt_interlocutor.format(idea = state['idea1'])
        
        # Set final messages and get the response
        messages = [SystemMessage(system_message)] + messages
        response = self.llm.invoke(messages)

        # Convert the message to AI message and set metadata
        msg = AIMessage(content = response.content, response_metadata = response_metadata)

        return {'messages': msg, 'count': state['count'] + 1, 'messages_hist': msg}
    
    def interlocutor2(self, state: State):
        '''
        Second interlocutor node.

        :param state: Graph State.
        :type state: StateGraph class
        '''

        logging.info('---INTERLOCUTOR 2---')
        # Set messages and metadata variable
        messages = state['messages']
        response_metadata = {'interlocutor': 'Interlocutor2'}

        # Change the message type because AIs must alternate the messages type order
        for i, m in enumerate(messages):
            if isinstance(m, HumanMessage):
                messages[i] = AIMessage(content = m.content)
            if isinstance(m, AIMessage):
                messages[i] = HumanMessage(content = m.content)

        # Get summary if it is avaliable
        summary = state.get('summary', '')

        if summary:
            system_message = f'{self.system_prompt_interlocutor.format(idea = state['idea2'])}\n\nResumen de lo que habéis hablado anteriormente en el debate: {summary}'
        else:
            system_message = self.system_prompt_interlocutor.format(idea = state['idea2'])
        
        # Set final messages and get the response
        messages = [SystemMessage(system_message)] + messages
        response = self.llm.invoke(messages)

        # Convert the message to AI message and set metadata
        msg = AIMessage(content = response.content, response_metadata = response_metadata)

        return {'messages': msg, 'count': state['count'] + 1, 'messages_hist': msg}
    
    def should_continue(self, state: State) -> Literal['summarize_conversation', 'interlocutor2']:
        '''
        Return the next node to execute.

        :param state: Graph State.
        :type state: StateGraph class
        '''

        messages = state['messages']

        # If there are more than eight messages, then we summarize the conversation
        if len(messages) > 8:
            return 'summarize_conversation'
        # Otherwise we can just end
        else:
            return 'interlocutor2'
        
    def summarize_conversation(self, state: State):
        '''
        Summarize previous conversation.

        :param state: Graph State.
        :type state: StateGraph class
        '''

        logging.info('---SUMMARIZATION---')
        # First, we summarize the conversation
        summary = state.get('summary', '')

        if summary:
            # If a summary already exists, we use a different system prompt
            # to summarize it than if one didn't
            summary_message = (
                f'Este es un resumen de lo que se ha hablado hasta ahora en el debate: {summary}\n\n'
                'Extiende el resumen basándote en los nuevos mensajes:'
            )
        else:
            summary_message = '''Crea un resumen de la conversación anterior. Ayúdate de la siguiente frase de ejemplo
                                para generar el resumen: "En la conversación se ha hablado sobre
                                bla bla bla, donde un interlocutor defiende X y el otro interlocutor defiende Y...":'''

        messages = state['messages'] + [HumanMessage(content = summary_message)]
        response = self.llm.invoke(messages)

        # We now need to delete messages that we no longer want to show up
        # I will delete all but the last two messages, but you can change this
        delete_messages = [RemoveMessage(id = m.id) for m in state['messages'][:-2]]

        return {'summary': response.content, 'messages': delete_messages}
    
    def count_exceed(self, state: State) -> Literal['supervisor', 'interlocutor1']:
        '''
        Count the number of intervetions to determine if the debate must be finished.

        :param state: Graph State.
        :type state: StateGraph class
        '''

        # If count exceed the n parameter, then send the debate history to supervisor
        if state['count'] > self.n:
            return 'supervisor'
        else:
            return 'interlocutor1'
        
    def supervisor(self, state: State):
        '''
        Supervisor node.

        :param state: Graph State.
        :type state: StateGraph class
        '''

        logging.info('---SUPERVISOR---')
        # Set messages and metadata variables
        response_metadata = {'interlocutor': 'Supervisor'}
        messages = [SystemMessage(content = self.system_prompt_supervisor.format(idea1 = state['idea1'], idea2 = state['idea2']))] + state['messages_hist']

        # Get the response
        response = self.llm.invoke(messages)

        # Convert the message to AI message and set metadata
        msg = AIMessage(content = response.content, response_metadata = response_metadata)

        return {'messages': msg, 'messages_hist': msg}
    
    def generate_app(self):
        '''
        Function to generate graph and compile the app.
        '''

        # Create the graph with nodes and edges
        logging.info('Generating graph...')
        graph = StateGraph(State)

        graph.add_node('interlocutor1', self.interlocutor1)
        graph.add_node('interlocutor2', self.interlocutor2)
        graph.add_node(self.summarize_conversation)
        graph.add_node('supervisor', self.supervisor)

        graph.add_edge(START, 'interlocutor2')

        graph.add_conditional_edges(
            'interlocutor2',
            self.count_exceed
        )

        graph.add_conditional_edges(
            'interlocutor1',
            self.should_continue
        )

        graph.add_edge('summarize_conversation', 'interlocutor2')

        graph.add_edge('supervisor', END)
        
        # Compile to app
        app = graph.compile()

        return app
    
    def init_debate(self):
        '''
        Function to init the debate.
        '''

        # The first intervention will be the first idea. Then the second interlocutor must refute it
        init_message = AIMessage(content = self.idea1, response_metadata = {'interlocutor': 'Interlocutor1'})

        logging.info('Generating app...')
        app = self.generate_app()

        # Config PDF to save the debate interventions
        pdf = FPDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Times', '', 12)
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)

        # Set the voices for the debate speech
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        # Select only spanish voices
        spanish_voices = [voice for voice in voices if 'Spanish' in voice.name]

        # If there are no spanish voices, then select available voices
        if not spanish_voices:
            spanish_voices = voices

        # Depending on the number of available voices, select different voices for each interlocutor
        num_voices = len(spanish_voices)
        if num_voices == 1:
            voice1 = voice2 = voice3 = spanish_voices[0].id
        elif num_voices == 2:
            voice1 = voice3 = spanish_voices[0].id
            voice2 = spanish_voices[1].id
        else:
            voice1 = spanish_voices[0].id
            voice2 = spanish_voices[1].id
            voice3 = spanish_voices[2].id

        messages = []

        # Get different messages by streaming the values of the graph
        for event in app.stream({'messages': init_message, 'count': 0, 'idea1': self.idea1, 'idea2': self.idea2}, stream_mode = 'values'):
            interlocutor = event['messages'][-1].response_metadata['interlocutor']
            message = event['messages'][-1].content
            logging.info(message)

            # Different voices for each interlocutor
            if interlocutor == 'Interlocutor1':
                engine.setProperty('voice', voice1)
            elif interlocutor == 'Interlocutor2':
                engine.setProperty('voice', voice2)
            elif interlocutor == 'Supervisor':
                engine.setProperty('voice', voice3)
            engine.say(message)
            engine.runAndWait()

            formatted_message = f'{interlocutor}: {message}'
            messages.append(formatted_message)

        # Write PDF with the debate
        for msg in messages:
            pdf.multi_cell(0, 10, msg.encode('utf-8', errors = 'replace').decode('utf-8'))
            pdf.ln(2)

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'debate_{timestamp}.pdf'

        pdf.output(f'./output/{filename}', 'S')
        