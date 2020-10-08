if(__name__ == "__main__"):
    print("Please run the AppOS.py file instead.")
else:
    from configparser import ConfigParser
    config = ConfigParser()
    file = "accinfo.ini"
    config.read(file)
    name = config["user"]["username"]
    pass1 = config["user"]["password"]
    app1e = config["app1"]["enabled"]
    app1n = config["app1"]["name"]
    import importlib
    userChoice = False
    print("""     _                       ___    ____  
    / \     _ __    _ __    / _ \  / ___| 
   / _ \   | '_ \  | '_ \  | | | | \___ \ 
  / ___ \  | |_) | | |_) | | |_| |  ___) |
 /_/   \_\ | .__/  | .__/   \___/  |____/ 
           |_|     |_|              """)
    print("But it's not an OS?")
    print("Beta 1.2.6")
    print("\n\nWelcome,\n\n")
    while userChoice == False:
        print("Please Choose Your User.\n\n")
        print("1. " + name + "\n\n0. Exit")
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
                        print("\n0. Settings")
                        if(app1e == "true"):
                            print("\n1. " + app1n)
                        print("\n\n#. Logout")
                        app = str(input())
                        if(app == "0"):
                            from assets import settings
                            settings.main()
                        if(app == "1" and app1e == "true"):
                            module = importlib.import_module("apps." + app1n)
                            module.run()
                        if(app == "#"):
                            appValid = True
                            passwordCorrect = True
                            userChoice = False
                        else:
                            print("Invalid App")
                else:
                    print("Incorrect Password")
        elif(userinput == "0"):
            exit()
        else:
            print("Invalid choice")
