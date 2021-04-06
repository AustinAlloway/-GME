import smtplib
def sendemail(to_email,user_displayname,user_email):
    try:
        password = "Diamondh4nd$"
        sender_email = "gme.matchmaking@gmail.com" # Enter your address
        
        SUBJECT = 'NEW MATCH FROM GME MATCH MAKING!!!'
        TEXT = """\
        Great News! You have been matched with {} and they have requested to communicate with you!
        Here is their email: {}.
        We hope something blossoms and you conversations go great!
        Sincerely,
            GME Match Making.""".format(user_displayname,user_email)
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