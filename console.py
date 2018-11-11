#!/usr/bin/python3
""" Entry point of the command interpreter
"""
import cmd


class HBNBCommand(cmd.Cmd):
    """ HBNBCommand class for command interpreter entry point.
    """
    intro = "Welcome to the hbnb. Type help to list commands.\n"
    prompt = "(hbnb) "

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

if __name__ == "__main__":
    HBNBCommand().cmdloop()
