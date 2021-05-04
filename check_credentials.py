import weakref
class Credentials():

    def check_credentials(self, **kwargs):
        # Get all our data
        login_type = kwargs["login_type"]

        # Variables that have to be checked
        first_name  = False
        last_name = False
        e_mail = False
        p_word = False

        is_cred_valid = False

        # Check if user entered a valid password via checking if its long enough
        def check_password(pass_w):
            is_pas_valid = False
            err_msg = ""

            if len(pass_w)<7:
                err_msg = "Password not strong enough!"
            elif len(pass_w)>7:
                is_pas_valid= True

            return is_pas_valid, err_msg

        # Check if user entered a valid email via .com
        def check_email(mail):
            is_mail_valid = False

            # Check for the dot com suffix
            if mail[-4:] != ".com":
                is_mail_valid = False
                error_msg = "Invalid email"
                
            elif mail[-4:] == ".com":
                is_mail_valid = True

            return is_mail_valid

        def check_names(name):
            is_name_valid = True
            num_in_name = 0

            # Loop through name
            for letter in name:
                try:
                    # This just checks if there are any numbers in the name
                    a_letter = isinstance(float(letter), float)
                    if a_letter:
                        num_in_name = num_in_name+1
                        
                except ValueError:
                    is_name_valid = True

            if num_in_name != 0:
                is_name_valid = False
                print(str(num_in_name))
            else:
                is_name_valid = True
                    
            return is_name_valid

        # Check first name and last name
        # Store names in a list

        #loop through names
        def name_check(name, num):
            name_valid = False
            # check if the user entered anything at all first
            name = name.__repr__.__self__

            
            if name.text == "":
                if num == 0:
                    name.hint_text = "Please enter first name!"
                    name.background_color = (1, 0.3686, 0.3686, 1)

                elif num == 1:
                    name.hint_text = "Please enter surname name!"
                    name.background_color = (1, 0.3686, 0.3686, 1)

            else:
                # Check if names dont have any number in them
                is_valid = check_names(name.text)

                if is_valid == False:
                    if num == 0:
                        name.hint_text = "Please enter a valid first name!"
                        name.background_color = (1, 0.3686, 0.3686, 1)

                    elif num == 1:
                        name.hint_text = "Please enter a  valid surname name!"
                        name.background_color = (1, 0.3686, 0.3686, 1)

                elif is_valid == True:
                    if num == 0:
                        name_valid = True
                        name.background_color = (1,1,1,1)

                    elif num == 1:
                        name_valid = True
                        name.background_color = (1,1,1,1)
            return name_valid

        # Check if email is valid

        # Check if user entered anything at all
        def email_check(email):
            email_valid = False
            if email.text == "":
                email.hint_text = "Please enter an email!"
                email.background_color = (1, 0.3686, 0.3686, 1)

            else:
                # Check if they entered a valid email
                is_mail = check_email(email.text)

                if is_mail == False:
                    email.hint_text = "Please enter a valid email!"
                    email.background_color = (1, 0.3686, 0.3686, 1)

                elif is_mail == True:
                    email.background_color = (1, 1, 1, 1)
                    email_valid = True
                    
            return email_valid


        # Now lastly check if password is valid

        #Check if the uder entered a password at all
        def password_check(password):
            pass_valid = False
            if password.text == "":
                password.hint_text = "Please enter a password!"
                password.background_color = (1, 0.3686, 0.3686, 1)

            else:
                # Check if they entered a valid password
                is_pass_valid, error_msg = check_password(password.text)

                if is_pass_valid == False:
                    password.text = ""
                    password.hint_text = "Password to weak!!"
                    password.background_color = (1, 0.3686, 0.3686, 1)

                elif is_pass_valid == True:
                    pass_valid = True
                    password.background_color = (1, 1, 1, 1)
            return pass_valid

        # Now use all the values we just got to see if we have a valid credential entry

        if login_type == "signin":
            f_name = kwargs["First_name"]
            l_name = kwargs["Last_name"]
            email = kwargs["Email"]
            password = kwargs["Password"]
            
            first_name = name_check(f_name, 0)
            last_name = name_check(l_name, 1)
            e_mail = email_check(email)
            p_word = password_check(password)
            
            # First check the names
            if first_name == True:

                # Now check th last name
                if last_name == True:

                    # Now check the email
                    if e_mail == True:

                        # Lastly check password
                        if p_word == True:
                            is_cred_valid = True
                        else:
                            print("Password is invalid")
                    else:
                        print("Email is invalid")
                else:
                    print("Last name is invalid")
            else:
                print("First name invalid!!")
                
        elif login_type == "login":
            f_name = kwargs["First_name"]
            password = kwargs["Password"]
            
          
            first_name = name_check(f_name, 0)
            p_word = password_check(password)

            if first_name == True:

                if p_word == True:
                    is_cred_valid = True
                else:
                    pass
            else:
                pass
            
        return is_cred_valid
                
                
