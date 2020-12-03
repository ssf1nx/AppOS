if __name__ == "__main__":
    print("Please run the AppOS.py file instead.")
else:
    def main():
        import getpass
        from configparser import ConfigParser
        config = ConfigParser()
        file = "accinfo.ini"
        config.read(file)
        app1e = config["app1"]["enabled"]
        pass1 = config["user"]["password"]
        appValid = True
        settings = True
        if(app1e == "true"):
            AppStatus = "Change"
        else:
            AppStatus = "Add"
        while settings == True:
            print("Please Choose an Option")
            print("\n1. Change your username\n2. Change your password")
            print("3. " + AppStatus + " App 1")
            if(app1e == "true"):
                print("4. Remove App 1")
            print("\n\n#. Credits\n\n0. Exit")
            settingsChoice = input()
            if(settingsChoice == "1"):
                print("\nPlease Enter Your New Username")
                name = str(input())
                config.set("user", "username", name)
                with open(file, "w") as configfile:
                    config.write(configfile)
                print("Changed!")
            elif(settingsChoice == "2"):
                settingsPassLoop = True
                while settingsPassLoop == True:
                    print("Please Enter Your Current Password")
                    settingsPass = getpass.getpass(prompt="")
                    if(settingsPass == pass1):
                        settingsPassLoop = False
                        newPassword = True
                        while newPassword == True:
                            print("\nPlease Enter Your New Password")
                            passConfirm = getpass.getpass(prompt="")
                            print("\nPlease Re-enter Your New Password")
                            passConfirm1 = getpass.getpass(prompt="")
                            if(passConfirm == passConfirm1):
                                newPassword = False
                                pass1 = passConfirm
                                config.set("user", "password", pass1)
                                print("Changed!")
                                with open(file, "w") as configfile:
                                    config.write(configfile)
                            else:
                                print("Password Does Not Match")
                    else:
                        print("Invalid Password")
            elif(settingsChoice == "#"):
                print("So far everything has been developed by Creep167 (Aeydin Reid).")
            elif(settingsChoice == "0"):
                settings = False
                appValid = False
            elif(settingsChoice == "3"):
                print("Please enter the name of the app")
                appname = str(input())
                print("Added!")
                print("Please Re-run this program to update changes.")
                config.set("app1", "enabled", "true")
                config.set("app1", "name", appname)
                with open(file, "w") as configfile:
                    config.write(configfile)
            elif(settingsChoice == "4" and app1e == "true"):
                config.set("app1", "enabled", "false")
                with open(file, "w") as configfile:
                    config.write(configfile)
                print("Removed App 1!")
                print("Please Re-run this program to update changes.")
            else:
                print("Invalid Choice")