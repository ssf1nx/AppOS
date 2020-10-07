if(__name__ == "__main__"):
    print("Please run the AppOS.py file instead.")
else:
    def main():
        import time
        from configparser import ConfigParser
        config = ConfigParser()

        file = "accinfo.ini"
        config.read(file)



        print("Importing DevTools...")
        time.sleep(2)
        print("Imported, installing...")
        for i in range(101):
            print(str(i) + "% installed,")
            time.sleep(0.1)
        print("Installed DevTools!")
        config.set("devtools", "enabled", "true")
        with open(file, "w") as configfile:
            config.write(configfile)