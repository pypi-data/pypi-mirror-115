from aitpi.input_initializer import InputInitializer
from aitpi.mirrored_json import MirroredJson
from aitpi.message import *
from aitpi.command_library import CommandLibrary
from aitpi.postal_service import PostalService
from aitpi.printer import Printer

class InputConverter():
    """Handles the map of input_unit buttons to commands, and sends messages accordingly
    """
    _inputUnits = None

    def __init__(self):
        """This is a static class
        """
        raise "Static class"

    @staticmethod
    def getMap():
        """Returns the map of input_unit

        Returns:
            [type]: [description]
        """
        return InputConverter._inputUnits

    @staticmethod
    def change(input_unit, command):
        """Called to change a input_unit's mapped command

        Args:
            input_unit (str): The 'button' to change
            command (str): The command to change to
        """
        Printer.print("Setting {} to {}".format(input_unit, command))

        # TODO: Should we add 'fixed' items?
        if (False):
            Printer.print("Cannot change input_unit {}".format(input_unit))
        elif (not CommandLibrary.contains(command)):
            Printer.print("Invalid command '{}'".format(command))
        elif (not input_unit in InputConverter._inputUnits.keys()):
            Printer.print("Invalid input_unit {}".format(input_unit))
        else:
            InputConverter._inputUnits[input_unit] = command

    @staticmethod
    def getIndex(name, key='name'):
        for index, i in enumerate(InputConverter._inputUnits._settings):
            if (i[key] == name):
                return index
        return -1

    @staticmethod
    def consume(msg):
        """Handles sending out commands when button is pressed

        Args:
            msg (str): The message containing the input_unit number
        """
        if (isinstance(msg,InputChangeRequest)):
            Printer.print("Change request not supported yet.")
            return
        input_unit = str(msg.data)
        i = InputConverter.getIndex(input_unit)
        if (i != -1):
            PostalService.sendMessage(CommandLibraryCommand(InputConverter._inputUnits[i]['reg_link'], msg.event))
        else:
            Printer.print("'{}' not a valid input".format(input_unit))


    @staticmethod
    def init(file):
        PostalService.addConsumer([InputCommand.msgId], PostalService.GLOBAL_SUBSCRIPTION, InputConverter)
        InputConverter._inputUnits = MirroredJson(file)
        uniqueList = []
        for index, input_unit in enumerate(InputConverter._inputUnits._settings):
            if (input_unit['type'] == 'encoder'):
                uniqueList.append(input_unit['left_trigger'])
                uniqueList.append(input_unit['right_trigger'])
            elif (input_unit['type'] == 'button'):
                uniqueList.append(input_unit['trigger'])
            else:
                Printer.print("'%s' type not supported" % input_unit['type'], Printer.ERROR)
            if (not CommandLibrary.contains(input_unit['reg_link'])
                and input_unit['reg_link'] != ''):
                Printer.print("Found invalid input_unit command '{}', removing...".format(input_unit['reg_link']))
                InputConverter._inputUnits[index]['reg_link'] = ''
        InputConverter._inputUnits.save()
        if (len(uniqueList) != len(set(uniqueList))):
            Printer.print("Duplicate triggers detected: ", Printer.ERROR)
            for dup in set(uniqueList):
                if (uniqueList.count(dup) > 1):
                    Printer.print(" '%s'" % dup)
        for index, input_unit in enumerate(InputConverter._inputUnits._settings):
            InputInitializer.initInput(input_unit)
        Printer.print("Input initialization complete!")
