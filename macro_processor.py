import os


#路徑處理
file_name = "MACRO.txt"
cd = os.getcwd()
input_path = os.path.join(cd, "input")
output_path = os.path.join(cd, "output")

instrustions = []
macro_content = []    #存放巨集內容
macro_dict = {}       #鍵:巨集名稱   值:巨集內容
is_macro = False

with open(os.path.join(input_path, file_name), encoding = "utf-8") as file:   #讀檔  將巨集的名稱及內容儲存
    print("processing " + file_name + "...\n")
    for line in file.readlines():
        line_list = line.upper().split()
        if line_list[0] != '.':
            #統一格式 => 標記欄(symbol)  指令(OP code) 運算元(operand)
            if len(line_list) == 2:
                line_list.insert(0, "")    
            if len(line_list) == 1:
                line_list.insert(0, "")    
                line_list.insert(2, "")    
            instrustions.append(line_list)
            if is_macro:
                macro_content.append(line_list)
            if line_list[1] == "MACRO":   
                is_macro = True
                macro_content.append(line_list)
            if line_list[1] == "MEND":
                is_macro = False
                macro_dict.update({macro_content[0][0]: macro_content})  #鍵:巨集名稱  值:巨集內容
                macro_content = []

output = ""
is_macro = False
for instruction in instrustions:
    if instruction[1] == "MACRO":  
        is_macro = True
    elif instruction[1] == "MEND":
        is_macro = False
        continue
    if is_macro:    #在巨集定義裡面  =>  跳過
        continue
    else:
        if instruction[1] in macro_dict.keys():   #有呼叫巨集  =>  要展開
            #print("%-10s%-10s%-s" % ("." + instruction[0], instruction[1], instruction[2])) #註解
            output += "." + instruction[0].ljust(9) + instruction[1].ljust(10) + instruction[2] + "\n"
            macro_content = macro_dict[instruction[1]]    
            real_parameters = instruction[2]     #實際要帶入的參數
            real_parameters_list = real_parameters.split(',')
            parameters = macro_content[0][2]     #巨集的形式參數
            parameters_list = parameters.split(',')
            #展開
            for i in range(1, len(macro_content) - 1):    
                content = macro_content[i].copy()   #不加上copy()會變成參照(pass by reference) 會修改到原來list的值
                for j in range(len(parameters_list)): 
                    content[2] = content[2].replace(parameters_list[j], real_parameters_list[j])  #帶入參數
                if i == 1:
                    #print("%-10s%-10s%-s" % (instruction[0], content[1], content[2]))
                    output += instruction[0].ljust(10) + content[1].ljust(10) + content[2] + "\n"
                else:
                    #print("%-10s%-10s%-s" % (content[0], content[1], content[2]))
                    output += content[0].ljust(10) + content[1].ljust(10) + content[2] + "\n"
        else:
            #print("%-10s%-10s%-s" % (instruction[0], instruction[1], instruction[2]))
            output += instruction[0].ljust(10) + instruction[1].ljust(10) + instruction[2] + "\n"
       
output_file_name = file_name.split(".")[0] + "_result.txt"
#輸出結果檔案
with open(os.path.join(output_path, output_file_name), 'w', encoding = "utf-8") as file:
    print("writing result in " + output_file_name + "\n") 
    for line in output:
        file.writelines(line)

print("finished ")



























