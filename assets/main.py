if(__name__ == "__main__"):
    print("Please run the AppOS.py file instead.")
else:
    from configparser import ConfigParser
    config = ConfigParser()
    file = "accinfo.ini"
    config.read(file)
    name = config["user"]["username"]
    pass1 = config["user"]["password"]
    userChoice = False
    print("     _                       ___    ____  \n    / \     _ __    _ __    / _ \  / ___| \n   / _ \   | '_ \  | '_ \  | | | | \___ \ \n  / ___ \  | |_) | | |_) | | |_| |  ___) |\n /_/   \_\ | .__/  | .__/   \___/  |____/ \n           |_|     |_|                    ")
    print("But it's not an OS?")
    print("Beta 1.2.6")
    print("\n\nWelcome,\n\n")
    while userChoice == False:
        print("Please Choose Your User.\n\n")
        print("1. " + name + "\n2. Guest\n\n0. Exit")
        userinput = input()
        if(userinput == "1"):
            userChoice = True
            passwordCorrect = False
            while passwordCorrect == False:
                print("Enter Password:")
                password = input()
                if(password == pass1):
                    passwordCorrect = True
                    appValid = False
                    while appValid == False:
                        print("Welcome " + name + ",")
                        print("Choose an app:")
                        print("\n0. Settings\n\n#. Logout")
                        app = str(input())
                        if(app == "0"):
                            from assets import settings
                            settings.main()
                        if(app == "#"):
                            appValid = True
                            passwordCorrect = True
                            userChoice = False
                        else:
                            print("Invalid App")
                else:
                    print("Incorrect Password")
        elif(userinput == "2"):
            userChoice = True
            print("guest")
            input()
        elif(userinput == "0"):
            exit()
        else:
            print("Invalid choice")
