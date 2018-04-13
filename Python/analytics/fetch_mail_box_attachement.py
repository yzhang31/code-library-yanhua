
import email
import getpass, imaplib
import os
import sys


def get_machine_name(filename):
    seps = str(filename).split("@")
    return seps[1]


if __name__ == '__main__':
    detach_dir = "D:\\"

    userName = 'SysMReceiver'
    passwd = 'd2018-slb@H1'

    #try:
    mailBox = imaplib.IMAP4_SSL('NL0230PF01N01.DIR.slb.com')
    typ, accountDetails = mailBox.login(userName, passwd)
    if typ != 'OK':
        print('Not able to sign in!')
        raise 1

    mailBox.select('Inbox')
    typ, data = mailBox.search(None, 'ALL')
    if typ != 'OK':
        print('Error searching Inbox.')
        raise 1

    total_count = len(data[0].split())
    current_pos = 0
    print("total email count is {0}".format(len(data[0])))

    # Iterating over all emails
    for msgId in data[0].split():
        print ("Fetching  {0:.2f}% progress".format(100*(current_pos/total_count )))
        typ, messageParts = mailBox.fetch(msgId, '(RFC822)')
        if typ != 'OK':
            print('Error fetching mail.')
            raise 1

        emailBody = messageParts[0][1]
        #mail = email.message_from_string(emailBody)
        mail = email.message_from_bytes(emailBody)
        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                # print part.as_string()
                continue
            if part.get('Content-Disposition') is None:
                # print part.as_string()
                continue
            fileName = part.get_filename()

            if bool(fileName):
                machine_name = get_machine_name(fileName)
                dest_dir = os.path.join(detach_dir, 'attachments', machine_name)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                file_path = os.path.join(dest_dir, fileName)
                if not os.path.isfile(file_path):
                    print("{0} - OK : {1}".format(current_pos, fileName))
                    fp = open(file_path, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                else:
                    print("{0} - Skip : {1}".format(current_pos, fileName))
        current_pos += 1;
        print(mailBox.store(msgId, '+FLAGS', '\\Deleted'))
        #mailBox.uid('STORE',msgId,'+FLAGS', '\\Deleted')
    mailBox.expunge()
    print("close and logout")
    mailBox.close()
    mailBox.logout()
