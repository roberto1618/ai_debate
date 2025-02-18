'''
State class to define main fields the graph will have.
'''

# Import libraries
from langgraph.graph.message import add_messages
from typing_extensions import Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph import MessagesState

class State(MessagesState):
    '''
    State class.
    '''
    # Summary of the debate last messages
    summary: str
    # Count to set when the debate is finished
    count: int
    # First idea to defend
    idea1: str
    # Second idea to defend
    idea2: str
    # Messages history to send to the supervisor so that it can get the final conclusion
    messages_hist: Annotated[list[AnyMessage], add_messages]