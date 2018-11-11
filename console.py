#!/usr/bin/python3
""" Entry point of the command interpreter
"""
import cmd
from models.base_model import BaseModel
import os
import models
import json

class HBNBCommand(cmd.Cmd):
    """ HBNBCommand class for command interpreter entry point.
    """
    intro = "Welcome to the hbnb. Type help to list commands.\n"
    prompt = "(hbnb) "

    class_dict = {'BaseModel': BaseModel}

    def do_quit(self, line):
        """ Returns true when the quit command is called
        """
        return True

    def do_EOF(self, line):
        """ Returns true when EOF command is called
        """
        return True

    def help_quit(self):
        """ Prints out instructions for quit command
        """
        print("Quit command to exit the program\n")

    def emptyline(self):
        """ pass when empty line and ENTER
        """
        pass

    def do_create(self, string):
        """ create a new instance base on valid class
        """
        str_split = string.split()
        if (len(str_split) == 0):
            print("** class name missing **")
        else:
            if str_split[0] not in HBNBCommand.class_dict.keys():
                print("** class doesn't exist **")
            else:
                for k, v in HBNBCommand.class_dict.items():
                    if k == str_split[0]:
                        new_instance = v()
                        new_instance.save()
                        print(new_instance.id)

    def do_show(self, string):
        """ represent the objects information base on class name and id number
        """
        str_split = string.split()
        name = "file.json"
        check = 0
        #name = models.engine.file_storage.FileStorage.__file_path
        if (len(str_split) == 0):
            print("** class name missing **")
        elif str_split[0] not in HBNBCommand.class_dict.keys():
            print("** class doesn't exist **")
        elif (len(str_split) == 1):
            print("** instance id missing **")
        else:
            if os.path.isfile(name):
                with open(name, 'r') as f:
                    dic = json.loads(f.read())
                    for k, v in dic.items():
                        if v['id'] == str_split[1]:
                            all_objs = models.storage.all()
                            for obj_id in all_objs.keys():
                                if str_split[1] == obj_id.split('.')[1]:
                                    print(all_objs[obj_id])
                                    check = 1
                                    break
            if check == 0:
                print("** no instance found **")

    def do_destroy(self, string):
        """ delete an instance based on class name and id number
        """
        str_split = string.split()
        name = "file.json"
        check = 0
        if (len(str_split) == 0):
            print("** class name missing **")
        elif str_split[0] not in HBNBCommand.class_dict.keys():
            print("** class doesn't exist **")
        elif (len(str_split) == 1):
            print("** instance id missing **")
        else:
            if os.path.isfile(name):
                with open(name, 'r') as f:
                    string = f.read()
                    dic = json.loads(string)
                with open(name, 'w') as f:
                    for k, v in dic.items():
                        if v['id'] == str_split[1]:
                            del dic[k]
                            del models.storage.all()[k]
                            if dic == {}:
                                os.remove(name)
                            else:
                                string = json.dumps(dic)
                                f.write(string)
                            check = 1
                            break
            if check == 0:
                print("** no instance found **")

    def do_all(self, string):
        str_split = string.split()
        name = "file.json"
        check = 0
        if len(str_split) == 1:
            if str_split[0] not in HBNBCommand.class_dict.keys():
                print("** class doesn't exist **")
            else:
                with open(name, 'r') as f:
                    dic = json.loads(f.read())
                all_objs = models.storage.all()
                for key in all_objs.keys():
                    if key.split('.')[0] == str_split[0]:
                        print(all_objs[key])
        else:
            all_objs = models.storage.all()
            for key in all_objs.keys():
                print(all_objs[key])

if __name__ == "__main__":
    HBNBCommand().cmdloop()
