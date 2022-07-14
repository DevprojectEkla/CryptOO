import smtplib
import ssl
from ssl import SSLContext, Purpose
import email.message
import email.utils
import os
# import subprocess
# import time attention ce module est importer via le module crypt_message il faut l'un ou l'autre
from crypt_message import *
import pathlib


class CryptoMail:
    def __init__(self):
        self.attribut1 = ""
    
    def initMail(self):
        pass
# from email.parser import BytesParser, Parser
# from email.policy import default

# maintype and subtype must be, for example: 'application', ".zip"
# or 'text' 'plain'
def auto_file_name(filename):
    local_time = str(email.utils.localtime()).split(".")[0].split(" ")

    date = local_time[0]
    hour = local_time[1].split(":")[0]
    minutes = local_time[1].split(":")[1]
    seconds = local_time[1].split(":")[2]

    auto_name = f"{date}" + "-" + f"{hour}h" + f"{minutes}" + f"({seconds})s" + filename

    return (auto_name)


def attach_file(message, p_maintype, p_subtype):
    while True:

        path_attached_filename = input("\n\tSelect your file for Attachment (fullpath\\filename)"
                                       "\n\t#CryptoMail> ")

        if os.path.isfile(path_attached_filename):
            attached_filename = os.path.basename(path_attached_filename)

            break

        else:
            print("\n\tHere you will have to choose a full correct path of the type\n\t"
                  "'c:\\Users\\Bob\\myfile.py")

    if message.is_multipart():
        pass

    else:
        message.make_alternative()
        message.add_header('Content-Disposition', 'attachment', filename=f'{attached_filename}')

    os.chdir(os.path.dirname(path_attached_filename))

    with open(f"{attached_filename}", "rb") as fb:
        attachment_content = fb.read()
        message.add_attachment(attachment_content, maintype=p_maintype, subtype=p_subtype,
                               filename=f'{attached_filename}')
        fb.close()
    return message


def modif_mail(message):
    input("\n\tDo you wan't to clear all attachments ('clear all'), to add another attachment (add), "
          "to modify your body text ('body')? \n\t(type 'clear all', 'add' or 'body' and press enter)"
          "\n\t#CryptoMail>")
    print("this function is not ready yet")
    pass


def set_mimetype(message, maintype, subtype):
    pass


def confirmation(question: str):
    while True:
        confirm = input(f"\n\t{question}  'y' or 'n':\n\n\t#CryptoMail>")
        if confirm == 'y':
            test = True
            break
        elif confirm == 'n':
            test = False

            break
        else:
            print("\n\tplease select 'y' or 'n':")

    return (test)


def crypto_mail():
    # on rentre les renseignements pris sur le site du fournisseur
    print("\n\n\n")
    presentation()
    time.sleep(1)
    chiffrement_StartTLS = False
    while True:
        while True:
            smtp_address = input(
                "\n\n\tchoose a server SMTP for the current session (ex:mx01.iliane.fr, smtp.gmail.com, smtp.orange.fr):\n\n\t#CryptoMail>")

            if smtp_address == "smtp.gmail.com" or smtp_address == "smtp.orange.fr":

                smtp_port = 465
                print("\n\tdefault port selected for smtp.orange.fr or gmail.com: 465")
                time.sleep(1)
                chiffrement_modif = confirmation("\n\tvoulez-vous activer le chiffrement StartTLS ?"
                                                 "\n\t(might be necessary for some smtp server\n\t but for selecting 'y' you have to know what you are doing)")
                if chiffrement_modif:
                    chiffrement_StartTLS = True
                    print("StartTLS crypting mode selected")
                else:
                    print("\n\tstandard TLS crypting mode selected")
                    pass
                break

            elif smtp_address == "mx01.iliane.fr":

                print("\n\tdefault port selected for smtp.mx01.iliane.fr: 587")
                smtp_port = 587
                chiffrement_StartTLS = True
                break


            elif smtp_address == 'smtp.office365.com':
                smtp_port = 587
                print("\n\tdefault port selected for smtp.office365: 587")
                chiffrement_StartTLS = True
                break

            else:
                while True:
                    while True:
                        smtp_port = input("\r\n\tchoose a specific port (ex:25):\n\n\t#CryptoMail>")
                        confirm = confirmation(f"\n\tconfirm port: {smtp_port} ?")
                        if confirm:
                            break
                        else:
                            continue

                    try:
                        smtp_port = int(smtp_port)
                        break

                    except:
                        print("\n\t The port number must be an int value...")
                        time.sleep(1)
            break

        # on rentre les informations sur notre adresse e-mail
        while True:
            myGoogleAccount = input("\r\n\tPlease enter your email address:\n\t#CryptoMail>")
            myPassWord = input("\r\n\tPasswd:")
            confirm = confirmation(f"\n\tconfirm login: {myGoogleAccount}:{myPassWord} ?")

            if confirm:
                break
            else:
                continue

        if confirm:
            break
        # confirm = confirmation(f"\n\tconfirm connexion to: {smtp_address}:{smtp_port} ?")
        # if confirm:
        ##   context = ssl.create_default_context()
        #  server = smtplib.SMTP_SSL(smtp_address, smtp_port, context=context)

        # try:
        #   server.login(myGoogleAccount, myPassWord)  # connexion au compte
        #  break

        # except smtplib.SMTPException:
        #    continue

        # else:
        #   continue
    # on rentre les informations sur le destinataire

    while True:
        email_receiver = input("\r\n\tenter the email of the receiver:\n\t#CryptoMail>")
        confirm = confirmation(f"\n\tconfirm receiver: {email_receiver} ?")

        if confirm:
            break
        else:
            continue

    # ce qui suit permet de donner un nom de fichier correspondant au mail envoyé date, destinateur/taire etc.

    local_time = str(email.utils.localtime()).split(".")[0].split(" ")
    date = local_time[0]
    hour = local_time[1].split(":")[0]
    minutes = local_time[1].split(":")[1]
    seconds = local_time[1].split(":")[2]

    fileName_local_time = f"{date}" + "-" + f"{hour}h" + f"{minutes}m" + f"{seconds}s"

    while True:

        mail_fileName = input(
            "\r\n\tChoose a .txt file for your mail or press enter to create a new Mail file:\n\t#CryptoMail>")

        newname = f"mail_" + f"{fileName_local_time}" + f"_From_{myGoogleAccount}_To_{email_receiver}.txt"
        if mail_fileName == "":

            with open(newname, "w") as fp:
                buffer = ""
                print("\n\n\t#CryptoMail> type your text here:")
                while True:
                    try:
                        line = input("\n\tnewline:")
                    except EOFError:
                        break
                    if not line:
                        break
                    content = buffer + f"\n{line}"
                    fp.write(content)
                fp.close()
                break

        # pour ouvrir un fichier txt et le prendre pour contenu du mail il faudrait ajouter:
        elif os.path.isfile(mail_fileName):
            with open(newname, 'w') as fp:
                content = open(mail_fileName, 'r').read()
                fp.write(content)
                fp.close()
                break

        else:
            print("\n\tplease type enter or a full path pointing to your file c:\\users\\Bob\\Mymail.txt")
            time.sleep(1)

    '''# If the e-mail headers are in a file, uncomment these two lines:
    # with open(messagefile, 'rb') as fp:
    # headers = BytesParser(policy=default).parse(fp)
    # Or for parsing headers in a string (this is an uncommon operation), use:
    headers = Parser(policy=default).parsestr(
        'From: Foo Bar <user@example.com>\n'
        'To: <someone_else@example.com>\n'
        'Subject: Test message\n'
        '\n'
        'Body would go here\n')
    '''
    # on pourrait créer une fonction encryptage pour les mails et l'appeler ici plutôt que
    # de tout faire à la mano comme cela...
    message = email.message.EmailMessage()

    with open(newname, 'r') as msg_file:
        encryption = False

        while True:
            choix = input("\n\t Do you want to encrypt your mail before sending?\n\t('y' or 'n'):\n\n\t#CryptoMail>")
            if choix == 'y':
                encryption = True
                key = generate_key()
                print(f"\n\tthis is the name of the file in clear text that will be encrypted:{newname}")
                my_path = os.getcwd()
                encrypted_mail = extract_str_and_encrypt(newname, my_path, key)

                try:
                    crypt_name = "encrypt_" + newname
                    with open(crypt_name, "w") as fd:
                        fd.write(encrypted_mail.decode("Utf8"))
                        fd.close()
                        open_notepad(crypt_name)
                        new_file = True
                        break

                except:
                    print(f"couldn't create a new file for {newname}")
                    print("\n\tyour mail has been successfully encrypted anyway.")
                    print(f"\n\t{encrypted_mail}")
                    new_file = False
                    break

            elif choix == 'n':
                print("\n\tNo encryption selected.")
                break

            else:
                print("\n\tplease select 'y' or 'n':")

        # notez qu'avec ce qui suit une version du mail non crypté est de toute façon sauvegardée
        # dans le dossier courant.

        if encryption:

            if new_file == True:
                with open(crypt_name, "r") as crypt_mail:
                    message.set_content(crypt_mail.read())
            else:
                message.set_content(encrypted_mail.decode("Utf8"))

        else:
            message.set_content(msg_file.read())

        objet = input("\n\tspecify the subject:")
        message['Subject'] = f'{objet}'
        message['From'] = myGoogleAccount
        message['To'] = email_receiver
        choix = input("\n\t Do you want to attach a file?  'y' or 'n'\n\n\t#CryptoMail>")
        while True:

            abort = False

            if choix == 'y':

                while True:  # this loop is broken when modify = False

                    modify = False
                    mime_type = (False, False)

                    while True:

                        p_maintype = input("\n\tset the maintype (must be 'text' or 'application'):\n\n\t#CryptoMail>")

                        if p_maintype in ('text', 'application'):

                            print(f"\n\tmaintype: {p_maintype}")
                            mime_type = (True, False)
                            break


                        else:
                            print(
                                "\n\tyou must choose one of the two options: 'text' or 'application' (without the '' )")

                    while True:

                        p_subtype = input(
                            "\n\tset the subtype (must be an extension (ex:'.txt', '.pdf', .zip, etc.):\n\n\t#CryptoMail>")

                        if p_subtype == "":
                            print("no subtype chosen")



                        elif p_subtype[0] == "." or p_subtype == "plain":
                            print("\n\tsubtype seems compatible")
                            mime_type = (True, True)
                            break



                        else:
                            print("\n\twrong subtype")

                    while True:
                        print(f"\n\tsubtype: {p_subtype}")

                        confirm = input(
                            f"\n\tDo you confirm this mime type: {p_maintype}/{p_subtype} ?  'y' or 'n':\n\n\t#CryptoMail>")
                        if confirm == 'y':
                            modify = False
                            break

                        elif confirm == 'n':
                            modify = True
                            print("\n\tyou can modify your mime type: maintype/subtype:")
                            break
                        else:
                            print("\n\tplease select 'y' or 'n':")

                    if modify:
                        print("\n\tyou can modify the selected mime type")


                    else:
                        break

                if mime_type == (True, True):

                    try:

                        message = attach_file(message, p_maintype, p_subtype)
                        print("\n\tattachment succeeded")
                        attachment = True

                    except:

                        attachment = False
                        print("could't attach the new file")

                else:
                    print("mime types have not been set properly")
                    while True:

                        condition = input("Do you wan't to try again (a) or abort attachment (b)?")
                        if condition == a:
                            abort = False
                            break

                        elif condition == b:
                            abort = True
                            break
                        else:
                            print("select 'a' or 'b' please.")

                choix = input("\n\t Do you want to attach another file?  'y' or 'n'\n\n\t#CryptoMail>")

                if abort:
                    break


            elif choix == 'n':
                print("\n\tno attachment selected")

                break

            else:
                choix = input(
                    "\n\tPlease you must answer 'y' or 'n'\n\t Do you want to attach another file?  'y' or 'n'\n\n\t#CryptoMail>")
                print("\n\tplease select 'y' or 'n':")

        print(f"\r\n\tHere is the mail you are about to send:\n\t{message}")
        time.sleep(3)

        print("\n\tle client va tenter la connexion au server en entrant les données d'identification")
        input("\n\tpress enter")

    # on crée la connexion
    # pour une connexion à un smtp utilisant microsoft exchange il faut se référer à la documentation MS.
    # quelque chose comme ce qui suit permet de se connecter avec ses identifiants (le handshake est réussi)
    # mais l'envoi de mail échoue probablement par ce que l'application elle-même est bloquée par la sécurité server.

    # EN CAS DE PROBLEME DE CONNEXION SSL TLS: voir aussi les options de server SMTP il faut autoriser des applications à se connecter.
    if chiffrement_StartTLS:
        print("\n\tChiffrement startTLS special mode started")
        time.sleep(1)
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)  # this is the context for defining a Secure Sockets Layer
            context.load_default_certs(purpose=Purpose.SERVER_AUTH)
            server = smtplib.SMTP(smtp_address, smtp_port)
            server.starttls(context=context)
            time.sleep(1)
        except:
            print("\n\tsecured connexion or authentication failed\n\n")
            print("\n\t[*] Trying the default_SSL context [*]")
            try:
                time.sleep(1)
                context = ssl.create_default_context()  # this is the context for defining a Secure Sockets Layer
                server = smtplib.SMTP(smtp_address, smtp_port)
                server.starttls(context=context)

            except:
                port = 465
                print(f"\n\n\t[*] trying another port:{port}  [*]")
                try:
                    time.sleep(1)
                    context = ssl.create_default_context()  # this is the context for defining a Secure Sockets Layer
                    server = smtplib.SMTP(smtp_address, port)
                    server.starttls(context=context)
                except:
                    try:
                        port = 25
                        print(f"\n\n\t[*] trying another port:{port}  [*]")
                        time.sleep(1)
                        context = ssl.create_default_context()  # this is the context for defining a Secure Sockets Layer
                        server = smtplib.SMTP(smtp_address, port)
                        server.starttls(context=context)

                    except:
                        print("\n\tcouldn't connect to the smtp server.\n\n\tTry to configure your server so that"
                              " it allows connections from other applications and try again.\n\n")



    else:
        print("\n\tChiffrement TLS standard started (ex: smtp.gmail.com)")
        time.sleep(1)

        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(smtp_address, smtp_port, context=context)

        # envoi du mail
    while True:
        ready = input("\n\tyour message is ready to send, do you want to send it ('y'),"
                      " modify it ('m') or exit ('q') ..?")
        if ready == "y":

            try:

                server.login(myGoogleAccount, myPassWord)  # uncomment this and comment the one in the begining
                # connexion au compte à la fin implique que si la connexion échoue tout le travail précéent est à refaire

                if message.is_attachment():  # i don't know if it is necessary, in one case, with attachment we send
                    # bytes in the other the mail is just string.
                    server.sendmail(myGoogleAccount, email_receiver, message.as_bytes())

                server.send_message(message, myGoogleAccount, email_receiver)  # .sendmail() or send_message(),
                # the first one needs a string for its message arg
                # the second wants a message object from EmailMessage Class
                # Be CAREFULL: the order of the ars is inverted (message,...) or (...,...,msg)
                print(f"\r\n\tyour mail has been successfully sent to: {email_receiver}")
                time.sleep(1)
                break

            except smtplib.SMTPException:
                print("\n\tyour mail couldn't be delivered")
                time.sleep(1)
                break

        elif ready == "m":
            modif_mail(message)
            print("\r\n\tthis option is not ready yet.")
        elif ready == "q":
            goodbye()
            time.sleep(3)
        else:
            print("\n\tplease select a correct answer")

    server.quit()


def presentation():
    try:
        Presentation = print(f"\n{open('Crypto_mail.txt', 'r').read()}")
        return (Presentation)
    except:
        print("Exception: could not find the presentation File")
        time.sleep(1)
        print("\n\n\tCrypto v.1.0: This is a simple program to encrypt and decrypt a text file."
              "\n\tby Fr. Raphael Boralevi")


if __name__ == '__main__':
    crypto_mail()

