#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from Settings_Module import MySettings
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "BeaverQueue"
Website = "https://www.streamlabs.com"
Description = "!beavers command"
Creator = "Metsfan"
Version = "1.0.0.0"

#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = MySettings()

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    global ScriptSettings
    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    ScriptSettings = MySettings(SettingsFile)
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command and Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User):
        Parent.SendStreamMessage("Time Remaining " + str(Parent.GetUserCooldownDuration(ScriptName,ScriptSettings.Command,data.User)))

    #   Check if the propper command is used, the command is not on cooldown and the user has permission to use the command
    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command and not Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User) and Parent.HasPermission(data.User,ScriptSettings.Permission,ScriptSettings.Info):
        # Parent.BroadcastWsEvent("EVENT_ADDED_TO_BEAVER_QUEUE","{'show':false}")
        command = data.GetParam(1)
        if command == 'list':
            print_list(data)
        elif command == 'addme':
            add_user(data)
        else:
            print_help(data)

        Parent.AddUserCooldown(ScriptName,ScriptSettings.Command,data.User,ScriptSettings.Cooldown)  # Put the command on cooldown

    
    return

def print_list(data):
    names = latest_names_queue()
    if len(names) > 0:
        Parent.SendStreamMessage("The next beavers to be born will be: {}".format(", ".join(names[0:5])))
    else:
        Parent.SendStreamMessage("The beaver queue is empty. Add yourself with !beavers addme to be born as a beaver!")

def add_user(data):
    names = latest_names_queue()
    if data.UserName in names:
        Parent.SendStreamMessage("{} is already in the queue. Please wait your turn!".format(data.UserName, data.GetParam(1)))
    else:
        add_name_to_queue(data.UserName)
        Parent.SendStreamMessage("{} has been added to the queue!".format(data.UserName, data.GetParam(1)))

def print_help(data):
    Parent.SendStreamMessage("Available Commands:\n!beavers addme - Add yourself as a beaver to be born!\n!beavers list - Display upcoming beavers")

def latest_names_queue():
    file = open(ScriptSettings.NamesFileLocation, "r")
    return [line.rstrip("\n") for line in file]

def add_name_to_queue(name):
    file = open(ScriptSettings.NamesFileLocation, "a")
    file.write(name + "\n")
    file.close()
#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    
    if "$myparameter" in parseString:
        return parseString.replace("$myparameter","I am a cat!")
    
    return parseString

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return
