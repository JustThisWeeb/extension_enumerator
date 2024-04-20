import os


def help():
    print("""
        Directory enumerator by jtw
-------------------------------------------------
This is a script that automatically enumerates a given directory and gives you a list of different information about it.
    
usage: [command] [directory]
    
Available commands:
help - this menu
extension - give a list of how many files with of all extensions found in the directory there are.
 - extension -r [directory] would make the command recursive and it would search all subdirectories. 
 - extension -s [directory] would make the command separate the files based off of popular formats (png, jpg, etc. in images; mp4, mov etc. in videos and others)
 - you can combine the two in a single command 
list - list out all files in a directory 
size - list out all files and their size in the given directory
exit or quit - exits the script 
  
""")

help()

command_list = ["help", "extension", "list", "size", "exit", "quit"] #just a quick list to compare to

# this is the main function ig.
def extension(directory: str, recursive:bool=False, separate:bool=False): #takes in the directory and the recursive and separate booleans
    ext_dict = {} #storing them in dictionaries seems optimal. Plus I like dictionaries
    if os.path.isdir(directory):
        list_the_directory = os.listdir(directory)
        for file in list_the_directory:
            if "." in file and not os.path.isdir(f"{directory}/{file}"): #there can still be false alerts. Especially some unzipped files can get through this but at least some false flags can be mitigated
                extension = file.split(".")[-1]
                if extension in ext_dict.keys():
                    ext_dict[extension] += 1
                else:
                    ext_dict[extension] = 1

        #recursive search of all subdirectories
        if recursive:
            recursive_search(directory=directory, dictionary=ext_dict,separate=separate, recursions=0) #recursions is just me keeping count of the loops it has gone through. If they reach a thousand in my opinion it should stop and reveal what it has found so far
            return "this was a recursive run.\n"
        else:
            if separate: #separate files if it's a non-recursive run (it would be faster & more efficient if one just wanted a count of the files in just that one specific directory)
                separate_files(ext_dict)
            else:
                string_of_extension_and_count = ""
                for extension, count in ext_dict.items():
                    string_of_extension_and_count += f"{extension}: {count} files\n"
                return string_of_extension_and_count
    else:
        return "File isn't a directory."

def separate_files(dictionary:dict): #separate files. I can add a lot more extensions to the list but it would make it more arbitrary probably. Plus those are just the most common ones. Every other extension just goes to others
    popular_formats = {"videos": ["mp4", "m4a", "mov", "gif"], "images": ["jpg", "png", "jfif", "jpeg"],
                       "audio": ["wav", "mp3", "flac"], "text": ["txt", "doc", "docx"], "executable": ["elf", "exe", "apk", "obb", "msi"],
                       "office": ["pdf", "pptx", "xls"], "virtualization": ["vmx", "ovf", "vdi", "vdmk"], "code": ["py", "cpp", "css", "php", "js", "kts"], "shortcuts": ["lnk", "url"]} #yes I added kotlin scratch files there don't judge me
    separated_dict = {}
    found_list = []
    for format in popular_formats.keys():
        for key in dictionary.keys():
            if key in popular_formats[format]:
                found_list.append(key)
                if format not in separated_dict.keys():
                    separated_dict[format] = [f"{key} - {dictionary[key]} files"]
                else:
                    separated_dict[format].append(f"{key} - {dictionary[key]} files")
    for key in dictionary.keys():
        if key not in found_list:
            if 'others' not in separated_dict.keys():
                separated_dict["others"] = []
            separated_dict["others"].append(f"{key} - {dictionary[key]} files")

    separated_string = ""
    for key, value in separated_dict.items():
        separated_string += "\n" + key + ":\n" + "\n".join(separated_dict[key]) + "\n" #this would look nicer with string formatting but for some reason I just decided to do that.
    print(separated_string)



def recursive_search(directory:str, dictionary:dict, recursions: int, separate:bool=False , dir_list=[]):
    if os.path.isdir(directory):
        list_the_directory = os.listdir(directory)
        for file in list_the_directory:
            if "." in file:
                extension = file.split(".")[-1]
                if extension in dictionary.keys():
                    dictionary[extension] += 1
                else:
                    dictionary[extension] = 1
            else:
                dir_list.append(directory+"\\"+file)

    if recursions >= 1:
        dir_list.remove(directory)
    if len(dir_list) == 0:
        if separate:
            separate_files(dictionary)
            return "recursive"
        else:
            string_of_extension_and_count = ""
            for extension, count in dictionary.items():
                string_of_extension_and_count += f"{extension}: {count} files\n"
            print(string_of_extension_and_count)
            return string_of_extension_and_count

    if recursions == 1000: #force stopping the recursions after they hit 1000 as otherwise it becomes too taxing on the system
        if separate:
            separate_files(dictionary)
            return "found"
        else:
            string_of_extension_and_count = ""
            for extension, count in dictionary.items():
                string_of_extension_and_count += f"{extension}: {count} times\n"
            string_of_extension_and_count += "\n\nEncountered an error while doing the recursive search: too many recursions (1000)\n"
            return "too many"
    recursions += 1
    recursive_search(directory=dir_list[0], dictionary=dictionary, dir_list=dir_list, recursions=recursions, separate=separate)




def list_enum(directory: str): #well that's an incredibly long function. also not sure why someone would choose this over the dir or ls commands. Both offer much more info than this and are builtin but I thought that a directory enumerator without these is just incomplete
    return "\n".join(os.listdir(directory))


def size(directory:str): #this too.
    path_list = os.listdir(directory)
    sizes_list = []
    for file in path_list:
        sizes_list.append(f"{file} - {os.path.getsize(f'{directory}/{file}')} bytes")
    return "\n".join(sizes_list)


#main loop
while True:
    user_in = input("command: ").split(" ")
    if "help" in user_in[0]:
        help()
    else:
        command = user_in[0]
        directory = user_in[-1]

    if command == "extension": #literally the only command that would actually get used
        if "-r" in user_in and "-s" in user_in:
            print("result will be recursive and separated.")
            print(extension(directory=directory, recursive=True, separate=True))
        elif '-r' in user_in:
            print(extension(directory=directory, recursive=True))
        elif "-s" in user_in:
            print(extension(directory=directory, separate=True))
        else:
            print(extension(directory))

    elif command == "list":
        print(list_enum(directory))
    elif command == "size":
        print(size(directory))

    elif command == "exit" or command == "quit":
        print("exiting script")
        exit()
    else:
        print("unknown command.")
        # command suggestion little algorithm - doesn't really work right. Didn't really try seriously either though
        found_match = False
        for pos_command in command_list:
            if found_match:
                break
            counter = 0
            for letter in command:
                if letter in pos_command:
                    counter+=1
            if counter == len(pos_command) or counter > len(pos_command) - 2:
                print(f"Did you mean {pos_command}? (this may be quite inaccurate lol)\n\n")
                found_match = True
                break
