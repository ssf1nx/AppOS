import os
import re
import time
import urllib.request as urllib
import getpass
import secrets
import hashlib
import base64
from configparser import ConfigParser

# localOnly is used for debugging version checker.
localOnly = False
config = ConfigParser()
file = "accinfo.ini"

# Version (duh).
__version__ = "2.0.1"

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
                            input("Enter to continue...")

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


    # Updates the accinfo.ini when it's outdated.
    def updateConfig(configVer):

        # If the config's version is 2.0.0 (last version), then upgrade it like this.
        if configVer == (2, 0, 0):
            
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

            # Writes to file.
            with open("accinfo.ini", "w") as configfile:
                config.write(configfile)

        # If the config's version is something else, unable to handle it.
        else:
            
            clearTerm()
            print("Unable to upgrade accinfo.ini. Please delete it to continue.")
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
                Apps.options(True)

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

            print("\n\nWelcome,\n\n") 
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
    def options(settings):

        clearTerm()

        while settings == True:
            clearTerm()

            print("Please Choose an Option")
            print("\n1. Change your username\n2. Change your password")
            print("\n\n#. Credits\n\n0. Exit\n")
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

                else:
                    print("\nInvalid Password")

                    time.sleep(1.5)

            # Very simple credits screen.
            elif settingsChoice == "#":
                clearTerm()

                print("Credits:\n\nDeveloped and Written by ssf1nx.\nGitHub: https://github.com/ssf1nx\n\n")
                input("Enter to go back...")

                clearTerm()

            # Exits the settings app back to the App Menu.
            elif settingsChoice == "0":
                settings = False
                appValid = False

            else:
                print("\nInvalid Choice")

                time.sleep(1.5)



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


# Clears the terminal on both Windows and Linux systems.
def clearTerm():
    os.system('cls' if os.name == 'nt' else 'clear')



# Calls Pre.update() for update check and then Pre.setupChecker() to check for the accinfo.ini file.
if __name__ == '__main__':
    accinfo = os.path.exists('accinfo.ini')

    # Checks for accinfo.ini and loads it if it exists.
    if accinfo == True:
        config.read(file)

    Pre.update()
    Pre.setupChecker()