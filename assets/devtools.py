if(__name__ == "__main__"):
    print("Please run the AppOS.py file instead.")
else:
    def main():
        from configparser import ConfigParser
        config = ConfigParser()
        file = "accinfo.ini"
        config.read(file)
        print("Config File")
        print(" user")
        print("username = " + config["user"]["username"])
        print("password = " + config["user"]["password"])
        print(" devtools")
        print("enabled = " + config["devtools"]["enabled"])
        devchoice = True
        while devchoice == True:
            print("\n\n1. Change something in 'user'\n2. Change something in 'devtools'\n0. Exit devtools")
            devchange = str(input())
            if(devchange == "1"):
                devchoice = False
                devchoice2 = True
                while devchoice2 == True:
                    print("\n1. Change 'username' value\n2. Change 'password' value\n0. Back")
                    devchange2 = str(input())
                    if(devchange2 == "1"):
                        print("Please enter the new value,")
                        username = str(input())
                        config.set("user", "username", username)
                        with open(file, "w") as configfile:
                            config.write(configfile)
                        print("Changed!")
                    elif(devchange2 == "2"):
                        print("Please enter the new value,")
                        password = str(input())
                        config.set("user", "password", password)
                        with open(file, "w") as configfile:
                            config.write(configfile)
                        print("Changed!")
                    elif(devchange2 == "0"):
                        devchoice2 = False
                        devchoice = True
                    else:
                        print("Invalid Choice")
            elif(devchange == "2"):
                devchoice = False
                devchoice3 = True
                while devchoice3 == True:
                    print("\n1. Change 'enabled' value\n0. Back")
                    devchange3 = str(input())
                    if(devchange3 == "1"):
                        print("Please enter the new value,")
                        enabled = str(input())
                        config.set("devtools", "enabled", enabled)
                        with open(file, "w") as configfile:
                            config.write(configfile)
                        print("Changed!")
                    elif(devchange3 == "0"):
                        devchoice3 = False
                        devchoice = True
                    else:
                        print("Invalid Choice")
            elif(devchange == "0"):
                devchoice = False