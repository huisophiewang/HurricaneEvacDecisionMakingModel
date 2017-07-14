COUNTIES = ['monroe county', 
            'bay county', 'escambia county', 'franklin county', 'gulf county',  'inland counties', 'okaloosa county',   'santa rosa county', 'walton county',
            'baldwin county','mobile county',
            'hancock county', 'harrison county','jackson county',
            'orleans parish', 'jefferson parish', 'plaquemines parish','st. bernard parish', 'st. charles parish', 'st. john the baptist parish', 'st. tammany parish']

STATES = ['FL Keys', 'FL Panhandle', 'AL', 'MS', 'LA']



def county_to_state(i):
    state = ''
    if i==0:
        state = 0
    elif i>=1 and i<=8:
        state = 1
    elif i>=9 and i<=10:
        state = 2
    elif i>=11 and i<=13:
        state = 3
    elif i>=14 and i<=20:
        state = 4
    return state
        
        
    