from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

#hide_debug_information()
set_website_title("Your Drafter Website")
set_website_framed(False)

@dataclass
class Structure:
    structure_name:str
    staining_molecule:str
    ratio:int
    
@dataclass
class State:
    treatment_groups:int
    data_points:int
    goal:str
    stain_molecules: list[Structure]
    
nucleus= Structure("Nucleus","Hoechst",500)
f_actin= Structure("F-actin","Rhodamine Phalloidin",50)
g_actin= Structure("G-actin","AlexaFluor488",200)
yap_taz= Structure("YAP/TAZ","AlexaFluor488",500)

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
        "Please enter the number of treatment groups that you plan to have (including control):\n",
        TextBox("user_groups",state.treatment_groups),
        "\n",
        "Please enter the number of data points that you would like for each treatment group:\n",
        TextBox("user_points",state.data_points),
        "\n",
        Button("BACK","home"),
        Button("NEXT","next_to_second_inputs")
    ])

@route
def next_to_second_inputs(state:State,user_groups:str,user_points:str)-> Page:
    state.treatment_groups=int(user_groups)
    state.data_points=int(user_points)
    user_molecules=[]
    return Page(state, [
        "Please select the goal of your experiment" + "\n",
        SelectBox("user_goal",
                  ["Find the percentage of a molecule that is in the nucleus","Find the ratio of G-actin to F-actin in the cell"],
                  state.goal),
        #edit the list above to contain more options, more accurate, etc.
        "\n",
        "Please select the molecules/structures that you would like to stain for:\n",
        CheckBox("check_nucleus"),
        "Nucleus\n",
        CheckBox("check_f_actin"),
        "F-actin\n",
        CheckBox("check_g_actin"),
        "G-actin\n",
        CheckBox("check_yap_taz"),
        "YAP/TAZ\n",
        #figure out how to make the checkbox values stay when you move pages
        Button("BACK","back_to_first_inputs"),
        Button("HOME","home"),
        Button("NEXT","next_to_results")
    ])

@route
def next_to_results(state:State,user_goal:str,check_nucleus:bool,check_f_actin:bool,check_g_actin:bool,check_yap_taz:bool)-> Page:
    #add checked molecules to state.stain_molecules
    state.goal=user_goal
    if check_nucleus:
        state.stain_molecules.append(nucleus)
    if check_f_actin:
        state.stain_molecules.append(f_actin)
    if check_g_actin:
        state.stain_molecules.append(g_actin)
    if check_yap_taz:
        state.stain_molecules.append(yap_taz)
    #iterate through the molecules in state.stain_molecules to create variables for all needed sections of the Structures
    #for molecule in state.stain_molecules:
        #if molecule==nucleus:
            #check_nucleus=True
        #elif molecule==f_actin:
            #check_f_actin=True
        #elif molecule==g_actin:
            #check_g_actin=True
        #elif molecule==yap_taz:
            #check_yap_taz=True
    #Modify a statement based on the goal
    if state.goal== "Find the percentage of a molecule that is in the nucleus":
        quant_2_statement= "in the nucleus vs. the cytoplasm"
        quant_4_statement= "nuclear/cytoplasmic integrated densities"
    elif state.goal== "Find the ratio of G-actin to F-actin in the cell":
        quant_2_statement="compared to the integrated density of ____ fluorescence"
        quant_4_statement="F-actin/G-actin integrated densities"
    #calculate quantities based on user goals for number of treatment groups and number of data points per group
    groups=state.treatment_groups
    points_per_group=state.data_points
    total_points=groups*points_per_group
    images_per_group=points_per_group//5
    images_per_dish=3
    dishes_per_group=images_per_group//images_per_dish
    dishes_needed=dishes_per_group*groups
    batches=3
    dishes_per_batch=dishes_needed//3
    return Page(state, [
        """
        Materials:
        
         - _____ extracted chondrocytes
         - """ +str(dishes_needed)+ """ individual glass dishes
         - _____ Permblock
         - _____ ___(structure1 primary antibody)___
         - Refrigerator with controlled temperature down to 4 ℃
         - _____ """+state.stain_molecules[0].staining_molecule+"""
         - _____ """+state.stain_molecules[1].staining_molecule+"""
         - _____ """+state.stain_molecules[2].staining_molecule+"""
         - _____ PBS
         - Aluminum foil container big enough to hold"""+str(dishes_per_group)+"""dishes of cells
         - _____ Drop-n-Stain
         - """+str(dishes_needed)+""" glass slides
         - Confocal microscope
         - Computer that works with confocal microscope


        Procedure:

        Primary and Secondary Staining
         1. Wash cultured chondrocytes with PBS and treat with Permblock for 15 minutes.
         2. Stain the chondrocytes with 200uL of primary antibody solution containing Permblock and a 1:___ ratio of ____(molecule)___ primary antibody (omit antibody if not staining for a specific molecule like YAP/TAZ?)
         3. Refrigerate the cells at 4 ℃ overnight.
         4. In the morning, make your secondary staining solution. Add Permblock and your secondary staining molecules at the proper ratios. For your experiment, this includes a 1:"""+str(state.stain_molecules[0].ratio)+""" ratio of """+state.stain_molecules[0].staining_molecule+""" to stain the """+state.stain_molecules[0].structure_name+""",
            a 1:"""+str(state.stain_molecules[1].ratio)+""" ratio of """+state.stain_molecules[1].staining_molecule+""" to stain the """+state.stain_molecules[1].structure_name+""", and a 1:"""+str(state.stain_molecules[2].ratio)+""" ratio of """+state.stain_molecules[2].staining_molecule+""" to stain the """+state.stain_molecules[2].structure_name+""".
         5. Wash the cells with PBS, and treat them with 200uL of the secondary staining solution that you made in step 4. Make sure to treat one dish with secondary stains but no primary antibodies. This allows you to identify non-specific binding. 
         6. Place the chondrocytes in a dark foil container for 1 hour at room temperature.
         7. Wash the chondrocytes with PBS. 
         8. Cover the cells on each dish with 1 drop of Drop-n-Stain and a glass slide.
         9. Refrigerate the cells in the dark at 4 ℃ until imaging.
         10. Repeat steps 1-9 with"""+str(batches-1)+""" more rounds of cells. It is recommended to perform the confocal microscopy (procedure below) for each batch of cells before staining the next batch of cells.

        Confocal Microscopy (Imaging)
         1. Make sure your confocal microscope ((LSM880) Airyscan Confocal Microscope recommended) and computer are turned on and calibrated. 
         2. Change the settings to take images of the cells at a 63× objective with a 1024 × 1024 pixel size
         3. Take 3 images from varying locations in each dish.
         4. Repeat steps 1-3 with the cells from each of your stain batches as you prepare them.

        Data Analysis
            Qualitative analysis:
             1. Choose 1 high-quality image from each treatment group (including the control) that visually represents the entire group.
             2. Display and describe the representative images next to each other to visually demonstrate the changes that have or have not occurred in molecule concentration or location.
            Quantitative analysis:
             1. Download the data analysis program FIJI.
             2. Use FIJI to find the integrated density of _____ fluorescence """+quant_2_statement+""". 
             3. In a spreadsheet program, normalize your fluorescence values to the average of the control values.
             4. Using a graphing program (Prism or JMP recommended), create a graph (One-Way ANOVA recommended) comparing your treatment groups (on the x-axis) to their corresponding normalized values of"""+quant_4_statement+"""
        """,
        "\n",
        Button("BACK","back_to_second_inputs"),
        Button("HOME","home"),
        Button("FINISH","next_to_finish")
    ])

@route
def next_to_finish(state:State)-> Page:
    return Page(state, [
        "Good luck on your experiment!\n",
        Button("RESTART","restart"),
        "\n",
        Button("BACK","back_to_results"),
    ])

@route
def home(state:State)-> Page:
    return index(state)

@route
def restart(state:State) -> Page:
    state.treatment_groups=0
    state.data_points=0
    state.goal=""
    state.stain_molecules=[]
    return index(state)
    
@route
def back_to_first_inputs(state:State)-> Page:
    return start(state)

@route
def back_to_second_inputs(state:State)-> Page:
    user_groups=state.treatment_groups
    user_points=state.data_points
    return next_to_second_inputs(state,user_groups,user_points)

@route
def back_to_results(state:State)-> Page:
    user_goal=state.goal
    check_nucleus=False
    check_f_actin=False
    check_g_actin=False
    check_yap_taz=False
    for molecule in state.stain_molecules:
        if molecule==nucleus:
            check_nucleus=True
        elif molecule==f_actin:
            check_f_actin=True
        elif molecule==g_actin:
            check_g_actin=True
        elif molecule==yap_taz:
            check_yap_taz=True
    return next_to_results(state,user_goal,check_nucleus,check_f_actin,check_g_actin,check_yap_taz)

start_server(State(0,0,"",[]))
