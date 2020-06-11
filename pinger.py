# ping address and tells if it could be connected to
# very self explanitory
# made for windows

from os import popen
from re import findall


def ping():
    addrPingTo = input("Input IP or Hostname: ")

    print("---| pinging... |---")

    cmdOut = findall("\d+", str(findall("\d+% loss", str(popen("ping " + addrPingTo).read()))))

    cmdOut = "".join(cmdOut)

    while True:
        try:
            int(cmdOut)
            break
        except ValueError:
            print("\nIP/Hostname " + addrPingTo + " can't be found.")
            x = input("\nPress ENTER to exit or any key and ENTER to go again...")
            if x != "":
                ping()
            else:
                exit()
    if int(cmdOut) == int("100"):
        input("The IP " + addrPingTo + " couldn't be reached.\n")
    else:
        print("The IP " + addrPingTo + " is currently online.\n")

    x = input("Press ENTER to exit or any key and ENTER to go again...")
    if x != "":
        ping()
    else:
        exit()
ping()
