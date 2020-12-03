if(__name__ == "__main__"):
    print("Please run the AppOS.py file instead.")
else:
    import getpass
    from configparser import ConfigParser
    config = ConfigParser()

    file = "accinfo.ini"
    config.read(file)

    print("Create a User\n")
    print("Please enter a username.")
    username = input()
    print("Please enter a password.")
    pass1 = getpass.getpass(prompt="")
    passCreate = True
    while passCreate == True:
        print("Please re-enter your password.")
        pass2 = getpass.getpass(prompt="")
        if(pass1 == pass2):
            passCreate = False
            config.add_section("user")
            config.set("user", "username", username)
            config.set("user", "password", pass1)
            config.add_section("app1")
            config.set("app1", "enabled", "false")
            config.set("app1", "name", "placeholder")

            with open(file, "w") as configfile:
                config.write(configfile)
            from assets import main
        else:
            print("Password Doesn't Match")
