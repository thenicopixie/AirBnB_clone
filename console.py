#!/usr/bin/python3
""" Entry point of the command interpreter
"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.review import Review
from models.place import Place
import os
import models
import json
import shlex


class HBNBCommand(cmd.Cmd):
    """ HBNBCommand class for command interpreter entry point.
    """
    intro = "Welcome to the hbnb. Type help to list commands.\n"
    prompt = "(hbnb) "

    class_dict = {'BaseModel': BaseModel, 'User': User, 'State': State,
                  'Amenity': Amenity, 'Place': Place, 'City': City,
                  'Review': Review}

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
        str_split = shlex.split(string)
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
        str_split = shlex.split(string)
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
        str_split = shlex.split(string)
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
                            string = json.dumps(dic)
                            f.write(string)
                            check = 1
                            break
            if check == 0:
                print("** no instance found **")

    def do_all(self, string):
        str_split = shlex.split(string)
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

    def do_update(self, string):
        """ Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file)
        """
        str_split = shlex.split(string)
        name = "file.json"
        check = 0
        dic = {}
        if (len(str_split) == 0):
            print("** class name missing **")
        elif str_split[0] not in HBNBCommand.class_dict.keys():
            print("** class doesn't exist **")
        elif (len(str_split) == 1):
            print("** instance id missing **")
        elif (len(str_split) == 2):
            print("** attribute name missing **")
        elif (len(str_split) == 3):
            print("** value missing **")
        else:
            if os.path.isfile(name):
                with open(name, 'r') as f:
                    dic = json.loads(f.read())
                    for key, value in dic.items():
                        if value['id'] == str_split[1]:
                            for k, v in dic[key].items():
                                if str_split[2] not in\
                                   ['id', 'created_at', 'updated_at']:
                                    all_objs = models.storage.all()
                                    setattr(all_objs[key], str_split[2],
                                            str_split[3])
                                    dic[key][str_split[2]] = str_split[3]
                                    check = 1
                                    break
                                else:
                                    check = 2
                                    print("** cannot update id, created_at or\
                                    updated_at attribute **")
                                    break
            if check == 1:
                with open(name, 'w') as f:
                    string = json.dumps(dic)
                    f.write(string)
            elif check == 0:
                print("** no instance found **")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
