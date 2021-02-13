# ping address and tells if it could be connected to
# very self explanitory
# made for windows

from os import popen
from re import findall


def ping():
    ping_address = input("Input IP or Hostname: ")

    print("pinging...")
    
    # this does, in order,
    # executes 'ping $ping_address' in Windows cmd_output
    # finds all substrings that match the regex '\d+% loss', in english being 'one or more of (+) any number (\d), followed by the string '% loss'
    # and lastly, removes the '% loss' literal, leaving only the number
    cmd_output = str(findall("\d+% loss", str(popen("ping " + ping_address).read()))).replace('% loss', '')

    cmd_output = "".join(cmd_output)

    while True:
        # try to keep pinging forever
        try:
            int(cmd_output)
            break
        # except when the IP/hostname doesnt exist/is invalid,
        except ValueError:
            print("\nIP/Hostname " + ping_address + " can't be found.")
            x = input("\nPress ENTER to exit or any key and ENTER to go again...")
            if x != "":
                ping()
            else:
                exit()
    # if 100% of the packets sent to $ping_address dont get returned, say its unreachable
    if int(cmd_output) == int("100"):
        input("The IP " + ping_address + " couldn't be reached.\n")
    # otherwise, they are reachable, theyre/youre just dropping the pings
    else:
        print("The IP " + ping_address + " is currently online.\n")

    x = input("Press ENTER to exit or any key and ENTER to go again...")
    if x != "":
        ping()
    else:
        exit()
ping()
