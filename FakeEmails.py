import ssl
import smtplib
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import signal
import time as t

class colors: #define colors
    Default      = "\033[39m"
    Black        = "\033[30m"
    Red          = "\033[31m"
    Green        = "\033[32m"
    Yellow       = "\033[33m"
    Blue         = "\033[34m"
    Magenta      = "\033[35m"
    Cyan         = "\033[36m"
    LightGray    = "\033[37m"
    DarkGray     = "\033[90m"
    LightRed     = "\033[91m"
    LightGreen   = "\033[92m"
    LightYellow  = "\033[93m"
    LightBlue    = "\033[94m"
    LightMagenta = "\033[95m"
    LightCyan    = "\033[96m"
    White        = "\033[97m"
    Bold         = "\033[1m"
    Underlined   = "\033[4m"
    END          = '\033[0m'

def ctrlc_handler(sig, frame): #ctrl + c detection
    print()
    print()
    print(colors.Red + "Goodbye!" + colors.END)
    print()
    exit()

signal.signal(signal.SIGINT, ctrlc_handler)


message = MIMEMultipart()

print()
sender = input(colors.LightBlue + "Real email address: ") #tva realna email adresa
#sender = "adamek.programator@email.cz"

#password = "HESLICKO200" #heslo na pevno, odtaguj, pokud ho chceš používat a zataguj getpasss
password = getpass.getpass("Real email password (invisible): ") #zepta se na heslo v terminalu, zataguj, pokud chces pouzivat pevne heslo

addressee = input("Real addressee: ") #na jakou adresu to posilas
#addressee = "tvojemama@example.com"

print(colors.END) #odbarveni

msgfrom = input(colors.LightYellow + "Fake name: ")
msgemail = input("Fake email: ")
msgreplies = input("Email for replies (you can leave it empty): ")
msgsubject = input("Subject: ")

print(colors.END)

#message["From"] = "Zeman <zeman@hrad.cz>" #name a email, email MUSI byt v <>
message["From"] = "{} <{}>".format(msgfrom, msgemail)
message["Reply-to"] = msgreplies
message["To"] = addressee
#message["Subject"] = "Pozdrav" #subject
message["Subject"] = msgsubject

print()
print(colors.Cyan + "Message (to finish rows, on the new row write \"//end\"):") #toto je message
row = ""
rownumber = 1
msg = ""
while row != "//end":
    row = input("Row {}: ".format(rownumber))
    if row != "//end":
        rownumber = rownumber + 1
        msg = "{}{}\n".format(msg, row)

msg = msg[:-1] #odstrani posledni \n v stringu
#print(msg)
print(colors.END)

smtp_server = "smtp.seznam.cz"

message.attach(MIMEText(msg))


#Toto je přípona image

if input(colors.Green + "Do you want to attach IMAGE attachment? (y/n): ") == "y":
    imagepath = input("ABSOLUTE path to the image and the name (eg. C:/images/file.png or /home/adam/Pictures/file.png): ")

    try:    
        myimage = open(imagepath, "rb") #pripona, musi to byt ABSOLUTNI cesta k obrazku, ne jen relativni ("obrazek.png") ale např. "C:/images/obrazek.png"
        image = MIMEImage(myimage.read())
        image.add_header('1', '1')
        message.attach(image)
        myimage.close()
    except:
        print()
        print()
        print(colors.Red + "************************************************************************************************")
        print("*No such file or directory! Check the image path: \"{}\"!*".format(imagepath))
        print("************************************************************************************************" + colors.END)
        print()
        print()
        exit()

    



#Toto je přípona text, muzes pouzit jakykoli format s utf-8 codecem (jakykoli textak, ale ne treba binarku)

myfile = open("/home/lukas/Documents/Python/Mailing/tst.py") #pripona, musi to byt ABSOLUTNI cesta k filu, ne jen relativni ("file.py") ale např. "C:/nevim_proste_neco_ve_windowsech/file.py"
text = MIMEText(myfile.read())
text.add_header("Content-Disposition", 'attachment; filename="{}"'.format("nazev.pripona")) #nastavitelna fake pripona a nazev
message.attach(text)
myfile.close()


print(colors.Magenta + colors.Bold + "Compiling email...")
context = ssl.create_default_context()
t.sleep(0.5)

print("Connecting to smtp.seznam.cz server..." + colors.END)
server = smtplib.SMTP_SSL(smtp_server, 465, context = context)
t.sleep(0.5)


with server:
    try:
        server.login(sender, password)
        print()
        print()
        print(colors.LightGreen + "****************************************************************************************************")
        print("*Succesfully authorized to account" + colors.END, colors.Magenta + sender + colors.END, colors.LightGreen + "with password" + colors.END, colors.Magenta + password)
        print(colors.LightGreen + "****************************************************************************************************" + colors.END)
        print()
        print()
    except:
        print()
        print()
        print(colors.Red + "************************************************************************************************************************")
        print("*Unable to authorize to account! Check your email -" + colors.END, colors.Magenta + sender + colors.END, colors.Red + "and your password -" + colors.END, colors.Magenta + password)
        print(colors.Red + "************************************************************************************************************************" + colors.END)
        print()
        print()
    t.sleep(0.5)
    try:
        server.sendmail(sender, addressee, message.as_string())
        print()
        print()
        print(colors.LightGreen + "***************************")
        print("*Message succesfully sent!*")
        print("***************************" + colors.END)
        print()
        print()
    except:
        print()
        print()
        print(colors.Red + "*********************************************")
        print("*Unable to send message! Some errors ocured.*")
        print("*********************************************" + colors.END)
        print()
        print()
