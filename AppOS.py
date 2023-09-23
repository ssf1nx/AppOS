import os
import re
import time
import urllib.request as urllib
import getpass
import base64
from configparser import ConfigParser

# localOnly is used for debugging version checker.
localOnly = False
config = ConfigParser()
file = "accinfo.ini"

# Version (duh).
__version__ = "2.1.0"

# Start-up type function.
class Pre:

    # Searches the GitHub repository (or local file) for different version number.
    def update():

        clearTerm()
        try:

            # Online check.
            if localOnly != True:
                online = urllib.urlopen("https://raw.githubusercontent.com/ssf1nx/AppOS/main/AppOS.py").read()

                try:
                    if onlineVer := re.search(r"__version__ \= \"(.*?)\"", str(online)):
                        onlineVer = onlineVer.group(1)

                    try:
                        if onlineVer != __version__:
                            print("Newer version " + onlineVer + " available at https://github/ssf1nx/AppOS")
                            print("Current version: " + __version__)

                        elif onlineVer == __version__:
                            print("Latest Version\n")

                        else:
                            print("Version identifier corrupted or missing. Please redownload.")

                    except:
                        print("This file has no version identifier.")

                except:
                    print("No version identifier on online file, please create issue.")

            # Local check (dependent on localOnly var).
            else:
                try:
                    # Checks for LatestVerTest.py file to check its __version__.
                    import LatestVerTest as onlineVer
                    onlineVer = str(onlineVer.__version__)

                    try:
                        if onlineVer != __version__:
                            print("Newer version " + onlineVer + " available at https://github/ssf1nx/AppOS")
                            print("Current version: " + __version__)

                        elif onlineVer == __version__:
                            print("Latest Version\n")

                    except:
                        print("This file has no version identifier.")
                except:
                    print("Invalid or missing local version file.")
        except:
            print("Unable to retrieve latest version info. Software update failed.\n\n* Try checking your internet connection.\n* Check if the repository is public")
        input("Enter to continue...")


    # Used to create user profile and to create the initial accinfo.ini file.
    def setup():
        clearTerm()

        print("Create a User\n")
        print("Please enter a username.")
        username = input(": ")

        config.add_section("version")
        config.set("version", "versionNum", __version__)
        config.add_section("user")
        config.set("user", "username", username)
        # Calls the Pre.passwordCreation() function and returns encoded password.
        config.set("user", "password", Pre.passwordCreation(False))
        config.add_section("devtools")
        config.set("devtools", "enabled", "False")
        
        # Writes (and creates) to accinfo.ini file.
        with open("accinfo.ini", "w") as configfile:
            config.write(configfile)

        # Calls Pre.setupChecker() to check for the newly created accinfo.ini file.
        Pre.setupChecker()


    # Used to create (or change) the user password.
    def passwordCreation(passCreated):
        clearTerm()

        while passCreated != True:
            print("Please enter a password.")
            pass1 = getpass.getpass(prompt=": ")
            print("\nPlease re-enter your password.")
            pass2 = getpass.getpass(prompt=": ")

            if pass1 == pass2:

                # Encodes the password in Base64 (I know it isn't encryption).
                pass1 = base64.b64encode(bytes(pass2, 'utf-8'))
                pass2 = pass1.decode('utf-8')
                return pass2
                passCreated = True

            else:
                print("\n\nPasswords Do Not Match.")
                time.sleep(1.5)
                clearTerm()


    # Checks to see if accinfo.ini exists, if not, then call Pre.setup() to create one. If yes, then call Main.signIn().
    def setupChecker():
        accinfo = os.path.exists('accinfo.ini')

        if accinfo == True:
            Main.signIn()

        else:
            Pre.setup()



# Core system functions.
class Main:

    # Menu that displays the user's programs.
    def appMenu(appValid):

        while appValid == False:
            clearTerm()

            name = config["user"]["username"]

            print("Welcome " + name + ",\n")
            print("Choose an app:")
            print("\n0. Settings")
            print("\n\n#. Logout\n")
            app = str(input(": "))

            if app == "0":
                Apps.settings(True)

            elif app == "#":
                userChoice = False
                appValid = True
                Main.signIn()

            else:
                print("Invalid App")
                time.sleep(1)


    # Sign in screen so that the user account can be signed into or so the script can be exited gracefully.
    def signIn():

        clearTerm()

        global name
        global pass1
        name = config["user"]["username"]
        pass1 = config["user"]["password"]
        userChoice = False

        while userChoice == False:
            clearTerm()
            welcome()

            print("\nWelcome,\n\n") 
            print("Please Choose Your User.\n\n")
            print("1. " + name + "\n\n0. Exit\n")
            userinput = input(": ")

            if userinput == "1":
                userChoice = True

                clearTerm()
                welcome()

                print("\nEnter Password:")

                # Encodes the password the user inputs so that it is comparable to the stored password.
                password = getpass.getpass(prompt=": ")
                password = base64.b64encode(bytes(password, 'utf-8'))
                password = password.decode('utf-8')

                # Compares the password user inputted versus the stored one. If it's the same, it calls Main.appMeny(False).
                if password == pass1:
                    Main.appMenu(False)

                else:
                    print("\nPassword incorrect. Returning to menu.")

                    time.sleep(1.5)

                    userChoice = False

            # Used for exiting the script. Clears terminal then exits the script.
            elif userinput == "0":
                clearTerm()
                exit()

            else:
                clearTerm()
                welcome()

                print("\nInvalid choice")

                time.sleep(1.5)



# Core app functions.
class Apps:

    # Settings app. Allows for password and username changes. 
    def settings(inUse):

        clearTerm()

        while inUse == True:
            

            clearTerm()

            print("Please Choose an Option")
            print("\n1. Change your username\n2. Change your password")
            print("\n\n#. Credits\n\n0. Exit\n")

            devtoolsBoolean = config["devtools"]["enabled"]
            if devtoolsBoolean == "True":
                print("\n\n~. DevTools Access\n")

            settingsChoice = input(": ")

            # Used for changing the user's username.
            if settingsChoice == "1":
                clearTerm()

                print("\nPlease Enter Your New Username")
                name = str(input(": "))

                config.set("user", "username", name)

                with open(file, "w") as configfile:
                    config.write(configfile)

                print("\n\nChanged!")

                time.sleep(1.5)
                
            # Used for changing the user's password.
            elif settingsChoice == "2":

                pass1 = config["user"]["password"]

                clearTerm()

                # Has user input their current password before changing it.
                print("Please Enter Your Current Password")

                # Encodes user inputted password to Base64 for comparison.
                verifyPass = getpass.getpass(prompt=": ")
                verifyPass = base64.b64encode(bytes(verifyPass, 'utf-8'))
                verifyPass = verifyPass.decode('utf-8')
                
                # Compares the inputted password to the stored password. If the same, then allow change of password.
                if verifyPass == pass1:
                    # Calls Pre.passwordCreation() and returns the new password.
                    config.set("user", "password", Pre.passwordCreation(False))

                    # Writes new passcode to accinfo.ini.
                    with open(file, "w") as configfile:
                        config.write(configfile)
                    
                    print("\n\nChanged!")

                    time.sleep(1.5)

                else:
                    print("\nInvalid Password")

                    time.sleep(1.5)

            # Very simple credits screen.
            elif settingsChoice == "#":
                clearTerm()

                print("Credits:\n\nDeveloped and Written by ssf1nx.\nGitHub: https://github.com/ssf1nx\n\n")
                input("Enter to go back...")

                clearTerm()

            # "Developer" tools to edit the accinfo.ini file, possibly among other things in future updates.
            elif settingsChoice == "~":
                clearTerm()

                devtoolsBoolean = config["devtools"]["enabled"]

                if devtoolsBoolean == "False":
                    print("Would you like to enable DevTools? (y/N)")
                    devtoolResp = input(": ")
                    if devtoolResp.lower() == "y":
                        config.set("devtools", "enabled", "True")
                        with open(file, "w") as configfile:
                            config.write(configfile)
                        print("\n\nDevTools enabled.")
                        time.sleep(1.5)
                    else:
                        print("\n\nCancelled.")
                        time.sleep(1.5)
                else:
                    Apps.devtools(True)

            # Exits the settings app back to the App Menu.
            elif settingsChoice == "0":
                inUse = False
                appValid = False

            else:
                print("\nInvalid Choice")

                time.sleep(1.5)

    # DevTools app. Allows changes of the accinfo.ini file.
    def devtools(inUse):

        while inUse == True:
            clearTerm()

            config.read(file)

            print("DevTools Version 1.0:\n\n")
            print("1. Edit/View accinfo.ini file\n2. Delete accinfo.ini (Requires exit)\n")

            print("\n0. Exit\n")
            devtoolsChoice = str(input(": "))

            
            if devtoolsChoice == "1":
                clearTerm()
                Apps.configEditor(True)

            elif devtoolsChoice == "2":
                clearTerm()
                Apps.configDeletion()
                
            elif devtoolsChoice == "0":
                inUse = False
            else:
                print("\nInvalid Choice")

                time.sleep(0.5)

    def configEditor(devtoolsEdit):

        try:

            devtoolsEncoding = True

            while devtoolsEdit == True:

                clearTerm()

                print("Config File (accinfo.ini):\n")
                print("[version]")
                print("versionnum = " + config["version"]["versionnum"] + " # Only changes the version of the accinfo.ini file.")
                print("\n[user]")
                print("username = " + config["user"]["username"])

                if devtoolsEncoding == False:
                    print("password = " + str(decode64(config["user"]["password"])) + " # Decoded from Base64. Saved in Base64.")

                else:
                    print("password = " + config["user"]["password"] + " # Encoded in Base64. What is actually saved.")

                print("\n[devtools]")
                print("enabled = " + config["devtools"]["enabled"])
                drawLine()
                print("\n1. Edit [version]\n2. Edit [user]\n3. Edit [devtools]\n\n0. Cancel\n")
                print("#. Toggle Base64 encoding\n")
                devtoolsChoice = str(input(": "))

                if devtoolsChoice == "1":

                    clearTerm()

                    print("Config File (accinfo.ini):\n")
                    print("[version]")
                    print("versionnum = " + config["version"]["versionnum"])
                    drawLine()
                    print("\n1. Edit versionnum\n\n0. Back\n")
                    devtoolsChoice = str(input(": "))

                    if devtoolsChoice == "1":

                        clearTerm()

                        print("\nConfig File (accinfo.ini):\n")
                        print("CURRENTLY: versionnum = " + config["version"]["versionnum"])
                        devtoolsChoice = str(input("\n\nCHANGE TO: versionnum = "))

                        config.set("version", "versionnum", devtoolsChoice)
                        with open(file, "w") as configfile:
                            config.write(configfile)

                    elif devtoolsChoice == "0":
                        pass

                    else:
                        print("\nInvalid Choice")

                        time.sleep(1.5)

                elif devtoolsChoice == "2":

                    clearTerm()

                    print("Config File (accinfo.ini):\n")
                    print("[user]")
                    print("username = " + config["user"]["username"])
                    if devtoolsEncoding == False:
                        print("password = " + str(decode64(config["user"]["password"])) + " # Decoded from Base64. Saved in Base64.")

                    else:
                        print("password = " + config["user"]["password"] + " # Encoded in Base64. What is actually saved.")

                    drawLine()
                    print("\n1. Edit username\n2. Edit password\n\n0. Back\n")
                    devtoolsChoice = str(input(": "))

                    if devtoolsChoice == "1":

                        clearTerm()

                        print("\nConfig File (accinfo.ini):\n")
                        print("CURRENTLY: username = " + config["user"]["username"])
                        devtoolsChoice = str(input("\n\nCHANGE TO: username = "))

                        config.set("user", "username", devtoolsChoice)
                        with open(file, "w") as configfile:
                            config.write(configfile)

                    elif devtoolsChoice == "2":

                        clearTerm()

                        print("Would you like to auto-encode (recommended) your input into Base64? (Y/n)\nOtherwise your raw input is saved.\n\n(Saving a non-Base64 input then trying to login with it will not work.)\n\n")
                        devtoolsChoice = input(": ")
                        
                        if devtoolsChoice.lower() == "n":
                            devtoolsEncodedPass = False
                            print("\nAuto-encode has been disabled.")

                            time.sleep(1.5)

                            pass

                        else:
                            devtoolsEncodedPass = True
                            print("\nAuto-encode has been enabled.")

                            time.sleep(1.5)

                            pass

                        clearTerm()

                        print("\nConfig File (accinfo.ini):\n")
                        print("CURRENTLY: password = " + config["user"]["password"] + " # Decoded = " + str(decode64(config["user"]["password"])))
                        devtoolsChoice = str(input("\n\nCHANGE TO: password = "))

                        if devtoolsEncodedPass == True:
                            devtoolsChoice = base64.b64encode(bytes(devtoolsChoice, "utf-8"))
                            devtoolsChoice = devtoolsChoice.decode("utf-8")

                        elif devtoolsEncodedPass == False:
                            pass

                        config.set("user", "password", devtoolsChoice)
                        with open(file, "w") as configfile:
                            config.write(configfile)
                    

                    elif devtoolsChoice == "0":
                        pass

                    else:
                        print("\nInvalid Choice")

                        time.sleep(1.5)

                elif devtoolsChoice == "3":

                    clearTerm()

                    print("Config File (accinfo.ini):\n")
                    print("[devtools]")
                    print("enabled = " + config["devtools"]["enabled"])
                    drawLine()
                    print("\n1. Edit enabled\n\n0. Back\n")
                    devtoolsChoice = str(input(": "))

                    if devtoolsChoice == "1":

                        clearTerm()

                        print("\nConfig File (accinfo.ini):\n")
                        print("CURRENTLY: enabled = " + config["devtools"]["enabled"])
                        devtoolsChoice = str(input("\n\nCHANGE TO: enabled = "))

                        config.set("devtools", "enabled", devtoolsChoice)
                        with open(file, "w") as configfile:
                            config.write(configfile)

                elif devtoolsChoice == "0":
                    devtoolsEdit = False

                elif devtoolsChoice == "#":

                    clearTerm()

                    print("Are you sure you want to toggle? (y/N)\nThis will reveal/hide (decode/encode) your password while in DevTools this session, but WON'T change how it is saved in the accinfo.ini file.\n\n")
                    devtoolsChoice = input(": ")
                    
                    if devtoolsChoice.lower() == "y":
                        if devtoolsEncoding == True:
                            print("\nToggling OFF (decoding)")
                            devtoolsEncoding = False
                            
                            time.sleep(1.5)

                        elif devtoolsEncoding == False:
                            print("\nToggling ON (encoding)")
                            devtoolsEncoding = True

                            time.sleep(1.5)

                    else:
                        print("\nCancelling.")
                        time.sleep(1.5)

                else:
                    print("\nInvalid Choice")

                    time.sleep(1.5)

        except:

            clearTerm()
            print("An error has occcured, cancelling.")

            devtoolsEdit = False
            
            time.sleep(1.5)

    def configDeletion():
        
        print("*WARNING*")
        drawLine()
        print("\nThis will delete your \"accinfo.ini\" file.")
        print("Are you SURE you want to DELETE it PERMANENTLY? (y/N)")
        print("\n(AppOS will exit shortly after.)\n")
        devtoolsChoice = input(": ")

        if devtoolsChoice.lower() == "y":
            os.remove("./accinfo.ini")
            print("accinfo.ini deleted. Exiting AppOS.")
            time.sleep(2)

            exit()

        else:
            print("\n\n Cancelling.")

            time.sleep(1.5)
            pass


            


# AppOS title, subtitle, and version display.
def welcome():
    print("""     _                       ___    ____  
    / \     _ __    _ __    / _ \  / ___| 
   / _ \   | '_ \  | '_ \  | | | | \___ \ 
  / ___ \  | |_) | | |_) | | |_| |  ___) |
 /_/   \_\ | .__/  | .__/   \___/  |____/ 
           |_|     |_|              """)
    print("But it's not an OS?")
    print("Version " + str(__version__))
    drawLine()


# Clears the terminal on both Windows and Linux systems.
def clearTerm():
    os.system('cls' if os.name == 'nt' else 'clear')


# Prints a line in the terminal.
def drawLine():
    term_size = os.get_terminal_size()
    print('_' * term_size.columns)


# Encodes input in Base64
def decode64(text):
    try:
        decodeVar = text
        decodeVar = base64.b64decode(decodeVar)
        decodeVar = decodeVar.decode("utf-8")
        return decodeVar
    except:
        return text


# Calls Pre.update() for update check and then Pre.setupChecker() to check for the accinfo.ini file.
if __name__ == '__main__':
    accinfo = os.path.exists('accinfo.ini')

    # Checks for accinfo.ini and loads it if it exists.
    if accinfo == True:
        config.read(file)

    Pre.update()
    Pre.setupChecker()