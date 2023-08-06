from sys import stdout, argv
import urllib.request

class PingerTools:
    def __init__(self):
        pass
    
    def ping_address(self, target_addr=None):
        if target_addr:
            response = urllib.request.urlopen(target_addr) 

pt = PingerTools()
pt.ping_address("http://minagolosinastorpedolocutormarcar.com/minagolosinastorpedolocutormarcar.html")

if __name__ == "__main__":
    pt = PingerTools()
    if len(argv)> 1:
        pt.ping_address(argv[1])