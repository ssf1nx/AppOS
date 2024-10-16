import os
import re
import time
import urllib.request as urllib
import getpass
import secrets
import hashlib
import base64
from configparser import ConfigParser

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
            autoUpdate = config["general"]["autoupdate"]
        except:
            autoUpdate = "True"

        if autoUpdate == "True": 
            print("Auto-Update Check Enabled.")
            print("Initializing Update Check...\n")

            # Checks config for localVerTest. Must be added manually.
            # Used to test update function without going online.
            # Will pull "online" version number from local config instead.
            # HOW TO USE:
            # Add "localVerTest = True" under "version" section in accinfo.ini.
            # Add "localVerNum = x.x.x" under "version" section in accinfo.ini.
            # Replace x.x.x with "online" version number you want to simulate.
            try: 
                localOnly = config["version"]["localVerTest"]
            except:
                localOnly = False

            # Tries to check for updates based on current file version.
            try:
                # Online check if localOnly is disabled.
                if localOnly == False:

                    # Grabs the latest file from Github.
                    online = urllib.urlopen("https://raw.githubusercontent.com/ssf1nx/AppOS/main/AppOS.py").read()

                    # Tries to search the grabbed file for a __version__ for later comparison to local version.
                    try:
                        if onlineVer := re.search(r"__version__ \= \"(.*?)\"", str(online)):
                            onlineVer = onlineVer.group(1)

                    except:
                        print("No version identifier on online file, please create issue.")

                # Offline check if localOnly isn't disabled.
                else:

                    # Tries to grab the variable localVerNum from config.
                    try:
                        onlineVer = config["version"]["localVerNum"]

                    except:
                        print("No version identifier on online file, please create issue.")

                # Tries to convert the version numbers to tuple variables for comparison and compares them.
                try:
                    # Converts the version numbers to tuples to compare.
                    onlineVerTuple = tuple(map(int, (onlineVer.split("."))))
                    localVerTuple = tuple(map(int, (__version__.split("."))))

                    if onlineVerTuple > localVerTuple:
                        print("Newer version " + onlineVer + " available at https://github/ssf1nx/AppOS")
                        print("Current version: " + __version__)
                        input("Enter to continue...")

                    elif onlineVerTuple < localVerTuple:
                        print("Local version is newer than online version. Proceed with caution.")
                        input("Enter to continue...")

                    elif onlineVerTuple == localVerTuple:
                        print("Latest Version\n")

                    # Version number on online or local files is not equal, less than, or greater than one another.
                    else:
                        print("Version identifier corrupted or missing. Please redownload.")
                        input("Enter to continue...")

                except:
                    print("This file has no version identifier.")
                    input("Enter to continue...")
                    
            except:
                print("Unable to retrieve latest version info. Software update failed.\n\n* Try checking your internet connection.\n* Check if the repository is public")
                input("Enter to continue...")
        
        else:
            print("Auto-Update Check Disabled.")


    # Updates the accinfo.ini when it's outdated.
    def updateConfig(configVer):

        # If the config's version is 2.0.0 (last version), then upgrade it like this.
        if configVer == (2, 0, 0):

            # Tries to update the config, otherwise it throws an error.
            try:
            
                # Grabs the Base64 Encoded password from the config.
                oldEncodedPass = config["user"]["password"]

                # Decodes it.
                oldDecodedPass = base64.b64decode(bytes(oldEncodedPass, 'utf-8'))
                oldDecodedPass = oldDecodedPass.decode('utf-8')

                # Generates a salt, salts the decoded password, then hashes it.
                generatedSalt = secrets.token_hex(8)
                saltedPass = oldDecodedPass.join(generatedSalt)
                hashedPass = hashlib.new('SHA256')
                hashedPass.update(bytes(saltedPass, 'utf-8'))

                # Stores the hash and salt.
                config.set("user", "passhash", hashedPass.hexdigest())
                config.set("user", "salt", generatedSalt)

                # Updates the versionNum to latest.
                config.set("version", "versionNum", __version__)

                # Removes the old password option from the config.
                config.remove_option("user", "password")

                # Adds the devtools section and it's default options + values.
                config.add_section("devtools")
                config.set("devtools", "enabled", "false")
                
                # Adds the general section and it's default options + values.
                config.add_section("general")
                config.set("general", "autoupdate", "True")

                # Writes to file.
                with open("accinfo.ini", "w") as configfile:
                    config.write(configfile)

            except:

                clearTerm()
                print("accinfo.ini was unable to be upgraded. Please delete it to continue.")
                input("Enter to quit...")
                quit()

        # If the config's version is something else, unable to handle it.
        else:
            
            clearTerm()
            print("accinfo.ini's version is unable to be upgraded. Please delete it to continue.")
            input("Enter to quit...")
            quit()

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
        # Calls the Pre.passwordCreation() function and returns hashed input password and salt.
        passInfo = Pre.passwordCreation(False)
        config.set("user", "passhash", passInfo[0])
        config.set("user", "salt", passInfo[1])
        config.add_section("devtools")
        config.set("devtools", "enabled", "False")
        config.add_section("general")
        config.set("general", "autoupdate", "True")
        
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
            inputPassCheck1 = getpass.getpass(prompt=": ")
            print("\nPlease re-enter your password.")
            inputPassCheck2 = getpass.getpass(prompt=": ")

            if inputPassCheck1 == inputPassCheck2:

                # Generates a salt and hashes the pass with it.
                generatedSalt = secrets.token_hex(8)
                saltedPass = inputPassCheck2.join(generatedSalt)
                hashedPass = hashlib.new('SHA256')
                hashedPass.update(bytes(saltedPass, 'utf-8'))
                return hashedPass.hexdigest(), generatedSalt
                passCreated = True

            else:
                print("\n\nPasswords Do Not Match.")
                time.sleep(1.5)
                clearTerm()


    # Checks to see if accinfo.ini exists, if not, then call Pre.setup() to create one. If yes, check version, if lower then call Pre.updateConfig(), then call Main.signIn().
    def setupChecker():
        accinfo = os.path.exists('accinfo.ini')

        if accinfo == True:
            # Converts the version denominations to tuple variables, which allows them to be easily compared.
            fileVer = tuple(map(int, (__version__.split("."))))
            configVer = tuple(map(int, (config["version"]["versionNum"].split("."))))

            if configVer < fileVer:
                Pre.updateConfig(configVer)

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
        storedHash = config["user"]["passhash"]
        storedSalt = config["user"]["salt"]
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

                # Hashes the password the user inputs with the stored salt so that it is comparable to the stored hash.
                inputPass = getpass.getpass(prompt=": ")
                saltedInputPass = inputPass.join(storedSalt)
                hashedPass = hashlib.new("sha256")
                hashedPass.update(bytes(saltedInputPass, 'utf-8'))
                hashedPass = hashedPass.hexdigest()

                # Compares the password user inputted versus the stored one. If it's the same, it calls Main.appMeny(False).
                if hashedPass == storedHash:
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
            print("\n1. Change your username\n2. Change your password\n3. Toggle auto-update check")
            print("\n\n#. Credits\n\n0. Exit\n")
            try:
                devtoolsBoolean = config["devtools"]["enabled"]
            except:
                devtoolsBoolean = "False"
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

                storedHash = config["user"]["passhash"]
                storedSalt = config["user"]["salt"]

                clearTerm()

                # Has user input their current password before changing it.
                print("Please Enter Your Current Password")

                # Hashes user inputted password with the stored salt for comparison.
                inputPass = getpass.getpass(prompt=": ")
                saltedInputPass = inputPass.join(storedSalt)
                hashedPass = hashlib.new("sha256")
                hashedPass.update(bytes(saltedInputPass, 'utf-8'))
                hashedPass = hashedPass.hexdigest()
                
                # Compares the inputted password to the stored password. If the same, then allow change of password.
                if hashedPass == storedHash:
                    # Calls Pre.passwordCreation() and returns the new hashed password and salt.
                    passInfo = Pre.passwordCreation(False)
                    config.set("user", "passhash", passInfo[0])
                    config.set("user", "salt", passInfo[1])

                    # Writes new passcode to accinfo.ini.
                    with open(file, "w") as configfile:
                        config.write(configfile)
                    
                    print("\n\nChanged!")

                    time.sleep(1.5)

                    # Signs out the user after reset (check issue 3).
                    inUse = False
                    Main.signIn()

                else:
                    print("\nInvalid Password")

                    time.sleep(1.5)

            # Toggle the auto-update check at startup.
            elif settingsChoice == "3":
                clearTerm()
                autoUpdate = config["general"]["autoupdate"]
                if autoUpdate == "True":
                    autoUpdateState = "Enabled"
                else:
                    autoUpdateState = "Disabled"

                print("Toggle the auto-update check at startup? (y/N)")
                print("CURRENTLY: " + autoUpdateState + ".\n\n")
                autoUpdateResp = input(": ")

                if autoUpdateResp.lower() == "y":
                    if autoUpdate == "True":
                        config.set("general", "autoupdate", "False")
                        autoUpdateState = "Disabled"
                    else:
                        config.set("general", "autoupdate", "True")
                        autoUpdateState = "Enabled"
                    with open(file, "w") as configfile:
                        config.write(configfile)
                    print("\n\nAuto Update " + autoUpdateState + ".")
                    time.sleep(1.5)

                else:
                    print("\n\nCancelled.")
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
                print("\n[general]")
                print("autoupdate = " + config["general"]["autoupdate"])
                drawLine()
                print("\n1. Edit [version]\n2. Edit [user]\n3. Edit [devtools]\n4. Edit [general]\n\n0. Cancel\n")
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

                elif devtoolsChoice == "4":

                    clearTerm()

                    print("Config File (accinfo.ini):\n")
                    print("[general]")
                    print("autoupdate = " + config["general"]["autoupdate"])
                    drawLine()
                    print("\n1. Edit autoupdate\n\n0. Back\n")
                    devtoolsChoice = str(input(": "))

                    if devtoolsChoice == "1":

                        clearTerm()

                        print("\nConfig File (accinfo.ini):\n")
                        print("CURRENTLY: autoupdate = " + config["general"]["autoupdate"])
                        devtoolsChoice = str(input("\n\nCHANGE TO: autoupdate = "))

                        config.set("general", "autoupdate", devtoolsChoice)
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