global the_cells
def read(x):#For TESTING PURPOSES
    file = open(x)
    file2 = open(x)
    lines = file.readlines()
    print(lines)
    #print(lines.index('        pin ("A") {\n'))
    #a = "hello"
    #b = a.replace('e' , '')
    #print(b)
def parser(x):
    file = open(x)
    file2 = open(x)
    lines = file.readlines()
    try:
        
        z, a = get_cell_names(lines)
        y = get_function_names(lines, a)
        
        footprints = get_footprint(lines, a)
        s = get_sequential(lines,a)
        l = get_latch(lines, a)
        pins = get_pin(lines, a)
        print(pins)
        the_cells = make_cells(z,y,footprints, s, l, pins)
        #print(the_cells)
        g = map_cells(the_cells)
        make_library(g, the_cells)
        
        
        
    finally:
        file.close()
    
    


def get_cell_names(lib_file):
    cell_names = []
    list = lib_file
    count_c = 0
    cell_divisions = []
    isComment = False
    for x in list:
        length = len(x)
        for y in range(length):
            if x[y:y+2] == '/*':
                isComment = True
                #print(isComment)
            #Assuming no nested comments symbols
                
            if x[y:y+2] == '*/':
                isComment = False
            if x[y:y+6] == 'cell (' and isComment == False:
                cell_divisions.append(list.index(x))
                count_c=count_c+1
                name_end = x.find(')')
                cell_names.append(x[y+6:name_end])
     
    return cell_names, cell_divisions

def get_function_names(lib_file, cell_positions):
    function_names = []
    function_count=0
    list = lib_file
    
    cell_divisions = cell_positions
    cell_divisions.append(len(list))
    
    function_found = False
    
    for p in range(len(cell_divisions)-1):
        function_found = False
        eachcell_function = [] 
        for a in list[cell_divisions[p]:cell_divisions[p+1]]:
            length = len(a)
            for b in range(length):
                if a[b:b+13] == ' function : "':
                    
                    function_found = True
                    function_count=function_count+1
                    function_end = a.find('";')
                    f = a[b+13:function_end]
                    #print(f)
                    new_f = ""
                    for letter in f:
                        if letter != " ":
                            new_f = new_f+letter
                            #print("")
                            

                    p_list = []
                    for letter in new_f:
                        if letter == "(" or letter == ")":
                            p_list.append(letter)
                

                    if new_f[0] == "(" and new_f[len(new_f)-1] == ")" and len(p_list) < 3:
                        new_f = new_f[1:len(new_f)-1]
                    eachcell_function.append(new_f)
        if function_found == False:
            function_names.append("No function")
        else:
            function_names.append(eachcell_function)
    
          
    return function_names                    

def get_footprint(lib_file, cell_positions):
    footprint_names = []
    footprint_count=0
    list = lib_file
    cell_divisions = cell_positions
    isComment = False
    for p in range(len(cell_divisions)-1):
        
        for x in list[cell_divisions[p]:cell_divisions[p+1]]:
            length = len(x)
            for y in range(length):
                if x[y:y+2] == '/*':
                    isComment = True
                if x[y:y+2] == '*/':
                    isComment = False
                if x[y:y+18] == 'cell_footprint : "' and isComment == False:
                    footprint_count = footprint_count+1
                    name_end = x.find('";')
                    footprint_names.append(x[y+18:name_end])
                    

    return footprint_names
    
            

def get_sequential(lib_file, cell_positions):
    sequential_cells = []
    #footprint_count=0
    list = lib_file
    cell_divisions = cell_positions
    isComment = False
    for p in range(len(cell_divisions)-1):
        seq_info = []
        isSequential = False
        for x in list[cell_divisions[p]:cell_divisions[p+1]]:
            length = len(x) 
            for y in range(length):
                if x[y:y+2] == '/*':
                    isComment = True
                    #print(isComment)
                #Assuming no nested comments symbols
                if x[y:y+2] == '*/':
                    isComment = False
                if x[y:y+4] == "ff (" and isComment == False:# number of functions: if 2 functions then Q
                    isSequential = True
                if x[y:y+14] == 'clocked_on : "' and isComment == False and isSequential == True: #Clock: I
                    clock_end = x.find('";')
                    seq_info.append(x[y+14:clear_end])
                if x[y:y+10] == 'preset : "' and isComment == False and isSequential == True: #Preset: S
                    preset_end = x.find('";')
                    seq_info.append(x[y+10:preset_end])
                if x[y:y+9] == 'clear : "' and isComment == False and isSequential == True: #Clear: R
                    clear_end = x.find('";')
                    seq_info.append(x[y+9:clear_end])
                if x[y:y+4] == "ff (" and isComment == False:# number of functions: if 2 functions then Q
                    seq_fun_end = x.find('")')
                    seq_info.append(x[y+4:seq_fun_end])
                    isSequential = True                                                     
                if x[y:y+14] == 'next_state : "' and isComment == False and isSequential == True: #Next State - nothing yet
                    state_end = x.find('";')
                    seq_info.append(x[y+14:state_end])
        
        sequential_cells.append(seq_info)
    #print(sequential_cells)
    return sequential_cells
                    
def get_latch(lib_file, cell_positions):
    latch_cells = []
    list = lib_file
    cell_divisions = cell_positions
    isComment = False
    for p in range(len(cell_divisions)-1):
        latch_info = []
        isLatch = False
        for x in list[cell_divisions[p]:cell_divisions[p+1]]:
            length = len(x)
            for y in range(length):
                if x[y:y+2] == '/*':
                    isComment = True
                if x[y:y+2] == '*/':
                    isComment = False
                if x[y:y+7] == "latch (" and isComment == False:# number of functions: if 2 functions then Q
                    latch_fun_end = x.find('")')
                    latch_info.append(x[y+7:latch_fun_end])
                    isLatch = True
                if x[y:y+10] == 'data_in : "' and isComment == False and isLatch == True:
                    latch_data_end = x.find('")')
                    latch_info.append(x[y+10:latch_data_end])
                if x[y:y+9] == 'clear : "' and isComment == False and isLatch == True:
                    latch_clear_end = x.find('";')
                    latch_info.append(x[y+9:latch_clear_end])
                if x[y:y+10] == 'preset : "' and isComment == False and isLatch == True: #Preset: S
                    latch_preset_end = x.find('";')
                    latch_info.append(x[y+10:latch_preset_end])
                if x[y:y+10] == 'enable : "' and isComment == False and isLatch == True: #Enable: I
                    latch_enable_end = x.find('";')
                    latch_info.append(x[y+10:latch_enable_end])
        latch_cells.append(latch_info)
    #print(latch_cells)
    return(latch_cells) 

def get_pin(lib_file, cell_positions):
    pin_cells = []
    lines = lib_file
    cell_divisions = cell_positions
    isComment = False
    for p in range(len(cell_divisions)-1):
        pin_info = [[],[]]
        for x in lines[cell_divisions[p]:cell_divisions[p+1]]:
            length = len(x)
            for y in range(length):
                if x[y:y+2] == '/*':
                    isComment = True
                if x[y:y+2] == '*/':
                    isComment = False
                if x[y:y+7] == ' pin ("' and isComment == False:
                    direction_found = False
                    #print("hi")
                    pin_end = x.find('")')
                    for c in lines[lines.index(x):cell_divisions[p+1]]:
                        line_length = len(c)
                        direction = ""
                        for b in range(line_length):
                            if c[b:b+13] == 'direction : "' and isComment == False and direction_found == False:
                                direction_found = True
                                dir_end = c.find('";')
                                direction = c[b+13:dir_end]
                        if direction == "input":
                            pin_info[0].append(x[y+7:pin_end])
                        if direction == "output":
                            pin_info[1].append(x[y+7:pin_end])
        pin_cells.append(pin_info)
    return pin_cells
                    
    
                
    
    
def make_cells(cells, functions, footprints, sequential, latch, pins):
   
    cell_dict = {}
    for x in cells:
        cell_info = []
        cell_info.append(functions[cells.index(x)])#0
        cell_info.append(footprints[cells.index(x)])#1
        cell_info.append(sequential[cells.index(x)])#2
        cell_info.append(latch[cells.index(x)])#3
        cell_info.append(pins[cells.index(x)])#4
        cell_dict[x] = cell_info
    return cell_dict
        
        
def map_cells(cells):
    gate_type = {}
    file_gate = open("gate_list.txt")
    gates = file_gate.readlines()
    print(cells) 
    for x in cells:
        
        if cells[x][2] == [] and cells[x][3] == []:
            #print("Print not sequential/latch")
            for name in gates:
                length = len(name)
                #print(length)
                for y in range(length):
                     if name[y:y+2] == 'Y=':
                         if cells[x][0][0] == name[y+2:length-1]:
                             
                             cell_name_end = name.find("\t")
                             #print(x + " is a " + name[:cell_name_end])
                             gate_type[x] = name[:cell_name_end]
                         
                
            
        elif cells[x][3] != []:
            cell_type = "LATCH"
            for y in cells[x][3]:
                if y == "!GATE_N":
                    cell_type+='I'
            for y in cells[x][3]:
                if y == "!S":
                    cell_type+='S'
            for y in cells[x][3]:
                if y == "!RESET_B":
                    cell_type+='R'
            for y in cells[x][3]:
                if y == '"IQ","IQ_N':
                    cell_type+='Q'
            #print(x + " is a " + cell_type)
            gate_type[x] = cell_type
        else:
            cell_type = "DFF"
            for y in cells[x][2]:
                if y == "!CL":#SHOULD BE !CLK_N SOMETHING WRONG IN GET_SEQUENTIAL
                    cell_type+='I'
            for y in cells[x][2]:
                if y == "!SET_B":
                    cell_type+='S'
            for y in cells[x][2]:
                if y == "!RESET_B":
                    cell_type+='R'
            for y in cells[x][2]:
                if y == '"IQ","IQ_N':
                    cell_type+='Q'
                
            #print(x + " is a " + cell_type)
            gate_type[x] = cell_type
    return gate_type
            
                
def make_library(gates, cells):
    #global the_cells
    print(gates)
    library = open("Library_Gates.txt")
    #library.close
    lines = library.readlines()
    library.close
    path = 'C:\\Users\\arjun\\OneDrive\\Documents\\Comp Sci Internship\\Sample_Library\\Test1.kicad_sym'
    sym = open(path, 'a')
    
    
    for gate in gates:
        sym_lines = []
        #print(gates[gate])
        for x in lines:
            
            if gates[gate] + "\n" == x:
                
                gate_start = lines.index(x)+1
                gate_end = ""
                found_end = False
                print("NEW GATE START:")
                print(gate_start)
                count = 0
                for c in lines[gate_start:]:
                    #print(c)
                    count = count+1
                    if c == "END\n" and found_end == False:
                        gate_end = lines[gate_start:].index(c)
                        found_end = True
                        
                print(gate_start)
                print(gate_end)
                for a in lines[gate_start:gate_start+gate_end]:
                    sym_lines.append(a)
                    #sym.write(a)
                for l in sym_lines:
                    l = l.replace(gates[gate], gate)
                    #symw.write(l)
                pin_count = 0
                for t in range(len(sym_lines)):
                    for p in range(len(sym_lines[t])):
                        if sym_lines[t][p:p+14] == "pin input line":  
                            print("GOT EM COACH")
                            print(cells[gate][4][0][pin_count])
                            
                            #print(sym_lines[t+1])
                            start = sym_lines[t+1].index('"')
                            print(start)
                            temp = sym_lines[t+1][:start+1]+ cells[gate][4][0][pin_count] + sym_lines[t+1][start+2:]
                            #print(temp)
                            sym_lines[t+1] = temp
                            print(sym_lines[t+1])


                            pin_count = pin_count+1
                for line in sym_lines:
                    sym.write(line)
                
                    
                
    sym.write(")")
                        
    
        

parser("sky130_Test5.lib")
#read("Library_Gates.txt")
