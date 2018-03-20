from GmailEngine.Cred_extract import Cred_extract

import base64
import email
from apiclient import errors

import httplib2
import os.path

from apiclient import discovery


class GmailMaster(object):

    def __init__(self,config):
        credentials = Cred_extract(config).credentials
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('gmail', 'v1', http=http)

    def view_labels(self):
        '''
        Methods shows list of label
            ID==>Name
        '''
        label_meta = self.service.users().labels().list(userId='me').execute()
        label_data = label_meta.get("labels")
        print("ID==>Name")
        for i in label_data:
            print("{0}==>{1}".format(i.get("id"),i.get("name")))

    def view_messages(self,label,q=None):
        '''
        Method shows list of messages in a label in following format
            ID:from:subject:date:attachment
        returns list of matching ids
        '''
        # list of messages
        if not q:
            message_meta = self.service.users().messages().list(userId='me',labelIds=label).execute()
        else:
            print("Using query: ",q)
            message_meta = self.service.users().messages().list(userId='me', labelIds=label,q=q).execute()
        message_data = message_meta.get("messages")

        id_list = []

        print("ID:from:subject:date:attachment")
        print("-------------------------------")

        counter = 0
        if message_data:
            for i in message_data:
                id = i.get("id")
                message = self.service.users().messages().get(userId='me', id=id).execute()  # getting message details
                #print(message.get("snippet"))
                #print(message.keys())
                from_str, date_str, subject_str, att_str = "", "", "", ""

                att_flag = False

                # flag for attachment
                try:

                    for i in message.get("payload").get("parts"):
                        if i.get("filename"):
                            att_flag =True
                            break
                except:

                    pass

                for j in (message.get("payload").get("headers")):

                    if j.get("name") == "From":  # from data
                        from_str = j.get("value")
                    elif j.get("name") == "Subject":  # Subject data
                        subject_str = j.get("value")
                    elif j.get("name") == "Date":  # Date data
                        date_str = j.get("value")

                output = "{0}:{1}:{2}:{3}:{4}".format(id,from_str,subject_str,date_str,att_flag)
                id_list.append(id)

                print(output)
                counter +=1

        print("-------------------------------")
        print("Total {} messages in label {}".format(counter,label))

        return id_list

    def download_attachment(self,msg_ids,STORE):
        '''
        Method for downloading attachment
        '''
        for msg_id in msg_ids:
            try:
                message = self.service.users().messages().get(userId='me', id=msg_id).execute()

                for part in message['payload']['parts']:
                    if part.get('filename'):
                        #file_data = base64.urlsafe_b64decode(part['body']['data'].encode('UTF-8'))
                        att_id = part.get("body").get("attachmentId")
                        attachment = self.service.users().messages().attachments()\
                            .get(userId='me', id=att_id,messageId=msg_id).execute()
                        #print(attachment)
                        file_data = base64.urlsafe_b64decode(attachment.get("data").encode('UTF-8'))
                        path = '/'.join([STORE, part['filename']])

                        f = open(path, 'wb')
                        f.write(file_data)
                        print("Downloading: ",os.path.basename(path))
                        f.close()


            except errors.HttpError as error:
                print("An error occurred:",error)

    def testing(self,label):
        '''
        Method for testing
        '''
        message_meta = self.service.users().messages().list(userId='me', labelIds=label)\
            .execute()
        message_data = message_meta.get("messages")

        for i in message_data:
            id = i.get("id")
            message = self.service.users().messages().get(userId="me", id=id,
                                                          format="raw").execute()

            #print(message)
            msg_str = base64.urlsafe_b64decode(message.get("raw").encode('ASCII'))
            mime_msg = email.message_from_string(msg_str.decode("utf-8"))


            with open("../OutputDir/check2.html","w") as f:
                f.write(str(mime_msg))
            #print(msg_str)
            #print(message.get("payload"))
            #print(message.keys())
            #for k in message.get("payload").get("parts"):
            #    if k.get("filename"):
            #       print("Present")
            break


if __name__ == "__main__":

    CONFIG = r"../Credentials/config.json"
    STORE = r"../OutputDir"
    QUERY = "from:hdfcbanksmartstatement@hdfcbank.net"
    
    #GmailMaster(CONFIG).view_labels()
    #GmailMaster(CONFIG).view_messages("Label_6")
    #print(GmailMaster(CONFIG).view_messages("INBOX"))
    #GmailMaster(CONFIG).testing("Label_6")
    #GmailMaster(CONFIG).testing("INBOX")
    #GmailMaster(CONFIG).download_attachment(["15446a1a2cfa0410"],STORE)
    #print(GmailMaster(CONFIG).view_messages("Label_6",QUERY))
    pass
