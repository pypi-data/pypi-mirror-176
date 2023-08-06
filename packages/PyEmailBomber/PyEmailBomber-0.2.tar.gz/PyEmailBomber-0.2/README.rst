

-- prerequisites

Follow the below steps to enable your gmail account to send emails.. 

This is necessary for sender only... No need to Follow the below steps for receiver email (client)

Step 1 : Go to your email settings

Step 2 : Click on the " Security " Tab

Step 3 : Turn on two step verification

Step 4 : Click on app passwords which is under two step verification option 

Step 5 : Give your email password and click on sign in

Step 6 : Now you will see your email device app passwords if you have any....

Step 7 : In the " select app " option menu, select Mail and in the " select device " option menu, select your OS (select 'Windows Computer' if you are windows system user)

Step 8 : Click on Generate

Step 9 : You will get 16 char long password, this is your mail account password. Use this password to send emails without interruption


Please check all the prerequisites above and continue the process

=======

How to use:
Create an object of Email class....

Call the send_mail() method with that object to send emails

Call the email_bomber() method with that object to send bulk emails

Methods:
-----------

.. code-block:: bash
    
    send_email(self, receiver : str, message : str, subject : str, filename = None)

    email_bomber(self, receivers:list[str], message:str, subject : str, count:int, time_lapse:int)

