import smtplib

#####################################################################################
# Param: email to send match message to, session user display name and email        #
# Function: Send email to the matched user specified by params                      #
# RETURNS: True if the email was sent and False if an error occurred                #
#####################################################################################
def sendemail(to_email,user_displayname,user_email):
    try:
        password = "Diamondh4nd$"
        sender_email = "gme.matchmaking@gmail.com" # Enter your address
        
        SUBJECT = 'YOU HAVE A NEW MATCH FROM GME!!'
        TEXT = """\
        Great News! You have been matched with {} and they have requested to communicate with you!
        Here is their email: {}.
        We hope something blossoms from your new found romance and you listen to music together.
        Sincerely,
            GME Match Maker.""".format(user_displayname,user_email)
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        conn = smtplib.SMTP('imap.gmail.com',587)
        conn.ehlo()
        conn.starttls()
        conn.login(sender_email, password)
        conn.sendmail(sender_email,to_email,message)
        conn.quit()
        return True
    except:
        return False