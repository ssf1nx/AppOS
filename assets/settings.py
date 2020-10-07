if __name__ == "__main__":
    print("Please run the AppOS.py file instead.")
else:
    def main():
        from configparser import ConfigParser
        config = ConfigParser()
        file = "accinfo.ini"
        config.read(file)
        pass1 = config["user"]["password"]
        appValid = True
        settings = True
        while settings == True:
            devtrue = config["devtools"]["enabled"]
            print("Please Choose an Option")
            print("\n1. Change your username\n2. Change your password\n\n#. Credits\n\n0. Exit")
            if(devtrue == "true"):
                print("\n\n\n~. DevTools Control Panel")
            settingsChoice = input()
            if(settingsChoice == "1"):
                print("\nPlease Enter Your New Username")
                name = input()
                config.set("user", "username", name)
                with open(file, "w") as configfile:
                    config.write(configfile)
                print("Changed!")
            elif(settingsChoice == "2"):
                settingsPassLoop = True
                while settingsPassLoop == True:
                    print("Please Enter Your Current Password")
                    settingsPass = input()
                    if(settingsPass == pass1):
                        settingsPassLoop = False
                        newPassword = True
                        while newPassword == True:
                            print("\nPlease Enter Your New Password")
                            passConfirm = input()
                            print("\nPlease Re-enter Your New Password")
                            passConfirm1 = input()
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
            elif(settingsChoice == "devtools.enabled = true"):
                if(devtrue == "false"):
                    settings = False
                    appValid = False
                    from assets import devtoolsinstall
                else:
                    print("Installed Already")
            elif(settingsChoice == "~" and devtrue == "true"):
                from assets import devtools
                devtools.main()
            else:
                print("Invalid Choice")
