from bakery import assert_equal
from drafter import *
from dataclasses import dataclass



hide_debug_information()
set_website_title("Your Drafter Website")
set_website_framed(False)

@dataclass
class Structure:
    structure_name:str
    staining_molecule:str
    ratio:int
    checked:bool
    
@dataclass
class State:
    treatment_groups:int
    data_points:int
    goal:str
    stain_molecules: list[Structure]

@route
def index(state: State) -> Page:
    return Page(state, [
        "Immunofluorescence Friend" + "\n",
        "Press the button to start!" + "\n",
        Button("BEGIN","start")
    ])

@route
def start(state:State)-> Page:
    return Page(state, [
        "Please enter the number of treatment groups" + "\n",
        "that you plan to have (including control):" + "\n",
        TextBox("user_groups"),
        "\n",
        "Please enter the number of data points that" + "\n",
        "you would like for each treatment group:" + "\n",
        TextBox("user_points"),
        "\n",
        Button("BACK","home"),
        "\n",
        Button("NEXT","next_to_second_inputs")
    ])

@route
def next_to_second_inputs(state:State,user_groups:str,user_points:str)-> Page:
    state.treatment_groups=int(user_groups),
    state.data_points=int(user_points)
    user_molecules=[]
    return Page(state, [
        "Please select the goal of your experiment" + "\n",
        SelectBox("user_goal",
                  ["Find the percentage of a molecule that is in the nucleus","Find the ratio of G-actin to F-actin in the cell"]),
        #edit the list above to contain more options, more accurate, etc.
        "\n",
        "Please select the molecules/structures" + "\n",
        "that you would like to stain for:" + "\n",
        CheckBox("nucleus"),
        "Nucleus\n",
        CheckBox("f_actin"),
        "F-actin\n",
        CheckBox("g_actin"),
        "G-actin\n",
        Button("BACK","home"),
        "\n",
        Button("NEXT","next_to_results")
    ])

@route
def next_to_results(state:State,user_goal:str)-> Page:
    state.goal=user_goal

@route
def next_to_finish(state:State)-> Page:
    pass

@route
def home(state:State)-> Page:
    pass

@route
def back_to_first_inputs(state:State)-> Page:
    pass

@route
def back_to_second_inputs(state:State)-> Page:
    pass

@route
def back_to_results(state:State)-> Page:
    pass

start_server(State(0,0,"",[]))
