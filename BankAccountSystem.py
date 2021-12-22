'''

Project Description: Develop a bank account management system where the user can check balance, deposit, withdraw, transfer money. The user can open a savings account or a checking account.
All the accounts created and updated are updated to accounts.txt
All the customers created are updated to customers.txt
All the transactions made are updated to accountsTransactions.txt

'''


# Class account to use the methods of a account management system.
class Account(object):
    """
    A class to represent a bank account system.

    ...

    Attributes
    ----------
    IBAN : str
        Accounts IBAN - used to transfer funds from one another
    acc_number : str
        Account Number of an account
    funds: int
        Amount of cash in an account
    signal: int
        Passed to check whether the account has been opened or created, if created - it writes to the file, if opened it updates the file
    num: int
        Passed to make iterating through the loop with less, more efficient code
    id: int
        Passed to use the customers ID from the customers file
    accounttype: str
        used to output to the file what type of account we're dealing with and how much we can overdraft
    transactions: str
        default value set to none so we can append any transactions to it when we call the methods

    Methods
    -------
    """

    # __init__ method used to assign values to the data members of the account class when the object is created
    def __init__(self, IBAN, acc_number, funds, signal, num, id, accounttype, transactions=None):
        """
        Constructs all the necessary attributes for the account object.

        Parameters
        ----------
            IBAN
            acc_number
            funds
            signal
            num
            id
            accounttype
            transactions
        """

        # assign the values to self

        self.IBAN = IBAN
        self.acc_number = acc_number
        # convert funds to an integer from a string
        funds = int(funds)
        self.funds = funds
        self.signal = signal
        self.num = num
        self.id = id
        self.accounttype = accounttype


        # if transactions was set to a default state, set transactions to have an empty list, else if values were passed to transactons, assign its value to self
        if transactions is None:
            self.transactions = []
        else:
            self.transactions = transactions

    # Withdraw method to take money of out the account
    def withdraw(self, amount):
        """
        Updates the funds in the account when taking money out of the account.

            Parameters:
                    amount (int): amount to be withdrawn from the account

            Returns:
                    "Can only withdraw a positive value" when amount is less than 0

            Updates:
                    Minus's the amount withdrawn from the funds
                    Checks if withdrawn amount exceeds account funds - Goes into overdraft
                    Appends the withdrawn message to transactions
        """
        # If amount asked to withdraw is not a positive integer value, do not allow user to withdraw amount
        if amount <= 0:
            print("You can only withdraw a positive value")
            return

        # Append the withdraw transaction made to transactions to be outputted to the file accountsTransactions.txt
        transaction = ("withdraw", amount)
        self.transactions.append(transaction)

        # Set over_draft to be the value of funds
        overdraft_check = self.funds

        # Minus the amount being withdrawn from the accounts funds
        self.funds -= amount

        # Check if the account type is savings account, if it is check if funds was reduced to less than 0, if it was tell the user you cannot go below 0 and set the funds back to its original value
        # Else if the account type is a checkings account, if it is check if funds was reduced to less than -500, checkings account overdraft is set to -500 and if this is exceeded, set the accounts funds to its original value
        if (self.accounttype == "Savings Account"):
            if(self.funds < 0):
                print("You cannot go beyond 0 in a savings account")
                self.funds = overdraft_check
            else:
                print("Amount withdrawn successfully")
        else:
            if(self.funds < -500):
                print("You cannot go beyond your -500 limit")
                self.funds = overdraft_check
            else:
                print("Amount withdrawn successfully")

    # Deposit method to take money of out the account
    def deposit(self, amount):
        """
        Updates the funds in the account when adding money to the account.

            Parameters:
                    amount (int): amount to be deposited to the account

            Returns:
                    "Can only deposit a positive value" when amount is less than 0

            Updates:
                    Adds the amount deposited to the funds
                    Appends the deposit message to transactions
        """

        # If amount asked to deposit is not a positive integer value, do not allow user to deposit amount
        if amount <= 0:
            print("You can only deposit a positive value")
            return

        # Append the deposit transaction made to transactions to be outputted to the file accountsTransactions.txt
        transaction = ("deposit", amount)
        self.transactions.append(transaction)

        # Add the amount being deposited to the accounts funds
        self.funds += amount

        print("Amount deposited successfully")


    # Transfer method to take money of out the account and send to another account using their IBAN
    def transfer(self, amount, IBAN):
        """
        Updates the funds in the account when transferring money to another account.

            Parameters:
                    amount (int): amount to be transfered to another account
                    IBAN (str): account to transfer and update the funds of the account

            Returns:
                    "Can only deposit a transfer value" when amount is less than 0

            Updates:
                    Minus's the amount transfered to the funds of the users account
                    Add's the amount transfered to the funds of the account its being sent to
                    Appends the transfer message to transactions
        """
        # Initalize accNumber2 to be used later
        accNumber2 = ""

        # If amount asked to transfer is not a positive integer value, do not allow user to transfer amount
        if amount <= 0:
            print("You can only transfer a positive value")
            return

        # read the account file and set the accNumber2 to be the value of the IBAN if the IBAN was found in the file
        f = open("accounts.txt", "r")
        index = 0
        num = 0

        for number, line in enumerate(f):
            index += 1

            if accNumber in line:
                accNumber2 = IBAN
                num = number

        # if IBAN wasnt found in the file let the user know, otherwise the IBAN was found and display this to the user
        if accNumber2 != IBAN:
            print("Unable to retrieve account")
            return
        else:
            print("Found account: ", accNumber2)

            # Iterate to 3 lines below the IBAN number to find the value of its funds
            num = num + 3
            with open('accounts.txt') as f:
                for i, line in enumerate(f, 1):
                    if i == num:
                        break
            funds = line

            # set funds2 to be the number found in this string
            funds2 = ''.join(x for x in funds if x.isdigit())

            # set funds3 to be the value the amount being sent to the acocunt added to its funds
            funds3 = int(funds2) + amount

            # read the accounts file again
            a_file = open("accounts.txt", "r")

            # set the list to contain all the text in the file
            list_of_lines = a_file.readlines()

            # update the funds value of the account being transferred the money
            list_of_lines[num-1] = "Account Funds: " + str(funds3) + "\n"
            a_file = open("accounts.txt", "w")
            a_file.writelines(list_of_lines)
            a_file.close

            # Append the transfer transaction made to transactions to be outputted to the file accountsTransactions.txt
            transfer = "Transfer to IBAN: " + str(IBAN)
            transaction = (transfer, amount)
            self.transactions.append(transaction)

            # Minus the amount being transferred from the accounts funds
            self.funds -= amount

    # __str__ method to output the account details and the account transactions to the external files
    def __str__(self):
        """
        Outputs the account details, transactions of the users account to the external files

            Returns:
                    The transactions made by the user to print to the user when the program is terminated.

            Updates:
                    The new account to the account file or updates the account details to an already opened account
        """

        # Assign the details of the account to result
        result = "-------------\nIBAN: " + self.IBAN + "\n"
        result += "Account number: " + str(self.acc_number) + "\n"
        result += "Funds: " + str(self.funds) + "\n"
        result += "Account Type: " + str(self.accounttype) + "\n"

        # if signal is 0 meaning that we are creating an account, write this to the end of the accounts.txt file, else if the signal is 1 meaning that we are updating an account being opened, update the value of its funds
        if signal == 0:
            lines = ["\nCustomer ID: " + str(self.id) + "\nIBAN: " + self.IBAN, "Account Number: " + str(self.acc_number), "Account Funds: " + str(self.funds), "Account Type: " + str(self.accounttype) + "\n-------------"]
            f = open("accounts.txt", "a")
            for line in lines:
                f.write(line)
                f.write('\n')
            f.close()
        elif signal == 1:
            filehandle = open("accounts.txt", "r")
            listOfLines = filehandle.readlines()
            lineNo = self.num
            listOfLines[lineNo-1] = "Account Funds: " + str(self.funds) + "\n"
            filehandle = open("accounts.txt", "w")
            filehandle.writelines(listOfLines)
            filehandle.close()
            print("Account updated")

        # Using a for loop to iterate through the first and last transactions made in the transactions list, output this list to the accountsTransactions.txt file
        last = len(self.transactions)
        first = last - 5
        if first < 0:
            first = 0

        #  if no transactions were made, return only the account details to the user when they exit the program
        if last == 0:
            return result

        result += "Transactions \n"
        for index in range(first, last):
            result += "#" + str(index+1) + " Type: " + self.transactions[index][0] + ". Amount: " + str(
                self.transactions[index][1]) + "\n"
            f = open("accountsTransactions.txt", "a")
            f.write(str(result))
            f.write('\n')

        # return the account details and transactions made to the user when they exit the program
        return result
        f.close()


# SavingsAcc is a subclass of the class account to represent the savings account of the user
class SavingsAcc(Account):

     # __init__ method used to assign values to the data members of the savings account class when the object is created

    def __init__(self, IBAN, acc_number, funds, signal, num, id, accounttype='Savings Account', transactions=None):

        # assign these values to the account parent class to differentiate what type of account is being used

        Account.__init__(self, IBAN, acc_number, funds, signal, num, id, accounttype, transactions)
        self.accounttype = accounttype

    def __str__(self):
        return_str = Account.__str__(self)

        return return_str

# CheckingAcc is a subclass of the class account to represent the checking account of the user
class CheckingAcc(Account):

    # assign these values to the account parent class to differentiate what type of account is being used

    def __init__(self, IBAN, acc_number, funds, signal, num, id, accounttype='Checking Account', transactions=None):
        Account.__init__(self, IBAN, acc_number, funds, signal, num, id, accounttype, transactions)
        self.accounttype = accounttype

    def __str__(self):
        return_str = Account.__str__(self)
        return return_str

# Customer class is a class used to collect the data of the customer to use when creating an account
class Customer():

    # __init__ method used to assign values to the data members of the customer class when the object is created

    def __init__(self,id,Name,Age,Address,accounts=[]):

        # assign the values to self

        self.id = id
        self.name = Name
        self.age = Age
        self.address = Address
        self.accounts = accounts

        # read the customers.txt file and output the account details to the end of the file, customerID of a new customer is incremented from the last customerID so we do not get duplicate customerID's

        a_file = open("customers.txt", "r")

        # put all the lines from customers.txt into lines
        lines = a_file.readlines()

        # Grab the second last line
        last_line = lines[-1:]
        lastline = last_line[0]

        #initalize lastline2 for taking the digit from line string

        lastline2 = ""

        # iterate through the string to grab the integer
        for word in lastline.split():
            if word.isdigit():
                lastline2 = lastline2 + word

        # increment the ID by 1

        id = int(lastline2) + 1

        # Display the customer ID to the user
        print("Your customer ID: ", id)

        # Write the customer details out to the customers.txt file
        file_members = open('customers.txt','a+')
        file_members.write("\nName: " + new_cust_name +"\n" +"Age: "+ str(new_cust_age) +"\n" + "Address: " + new_cust_address +'\n' + "customerID: " + str(id) + '\n')
        file_members.close()

    # __str__ method to output the customer details if customer is printed
    def __str__(self):
        result = "\nCustomerID: " + str(self.id)+ "\n"
        result += "Customer Name: " + self.name + "\n"
        result += "Age: " + str(self.age) + "\n"
        result += "Address: " + (self.address) + "\n\n"
        for index in range(len(self.accounts)):
            result += "Accounts: \n" + str(self.accounts[index])
        return result

# Initialize Variables
i = 0
count = 0
error_checking = 0

# Using a while to display menu to the user
while (i != 7):
    print('1. Create a new account\n')
    print('2. Deposit Cash\n')
    print('3. Withdraw\n')
    print('4. Open account\n')
    print('5. Add new customer\n')
    print('6. Transfer to another account\n')
    print('7. Exit\n')
    print('8. Help\n--------------\n')

    # Ask user which operation they want to carry out
    i = int(input('Please enter your operation: '))

    # If operation 1 was selected do the following:
    if i == 1:

        # As the user is creating an account, ask them what their IBAN, account number, initial funds, what type of account they want and their customer ID.
        IBAN = str(input("Please enter your new IBAN number: "))
        accNo = int(input("Please enter your new account number: "))
        funds = int(input("Please enter your initial funds: "))
        acc_type = input("Please enter 's' for savings or 'c' for checking accounts: ")
        id = int(input("Please enter your customer ID, Enter 0 if you don't remember your customer ID: "))

        # If they don't remember their customer ID, do the following
        if id == 0:

            # Ask them to enter their personal details in order to found out their customer ID

            name = str(input("Please enter your name: "))
            age = str(input("Please enter your age: "))

            # read through customers.txt file
            f = open("customers.txt", "r")

            # initialize variables
            index = 0
            index2 = 0
            name2 = ""
            age2 = ""

            # Find what number the name line is at
            for number, line in enumerate(f):
                index += 1

                if name in line:
                    name2 = name
                    num = number

            # Add two to this number and iterate through the file again to get the age
            num = num + 2
            num2 = num
            with open('customers.txt') as f:
                for i, line in enumerate(f, 1):
                    if i == num:
                        break
            age2 = line

            # Take the integer value inside the age string

            for word in age2.split():
                    if word.isdigit():
                        age2 = word

            # If the name and age details were not found for the customer, display this to the user. Else tell the user the account was found and grab the customer ID and age from the file and continue to create their specified account

            if name2 != name or age2 != age:
                print("Unable to find customer, you may want to add a new customer first by entering the '5' operation")
            else:
                print("Found account: ", name2)

                # Add two more lines to the number of lines to grab the customer ID of the user and iterate through the loop to the specific line and grab the line string
                num2 = num2 + 2
                with open('customers.txt') as f:
                    for i, line in enumerate(f, 1):
                        if i == num2:
                            break
                id = line

                # Extract the integer from the string to find the ID integer value
                for word in id.split():
                    if word.isdigit():
                        id = word

                # Display customer ID to the user so they know for next time
                print("Your customer ID is: ", id)

                # Set the variables back to their default values
                signal = 0
                index = 0
                num = 0

                # If s was enter create their savings account, else create their checking account
                if acc_type == 's':
                    # Pass their account details to the savings account class
                    acc_type = "Savings Account"
                    acc1 = SavingsAcc(IBAN, accNo, funds, signal, num, id, acc_type)
                else:
                    # Pass their account details to the checking account class
                    acc_type = "Checking Account"
                    acc1 = CheckingAcc(IBAN, accNo, funds, signal, num, id, acc_type)

                # Set error checking variable to be 1, incase the user tries to withdraw, deposit, transfer money when they havent created an account or opened one yet
                error_checking = 1

        # else if the user knows their customer ID proceed:
        else:

            # read through the customers file
            f = open("customers.txt", "r")

            # Initialize variables
            index = 0
            index2 = 0
            num = id

            # Set id2 to be the customerID string containing their ID
            # Set id3 default value to be validation string
            id2 = "customerID: " + str(id)
            id3 = "Couldnt find customer ID, Please make an account or enter 0 when creating an account to try find your customer ID"

            # Iterate through the file and set the line number to num to know which line the ID is found
            for number, line in enumerate(f):
                index += 1

                if id2 in line:
                    # If id is found set id3 to be the value of id and set num to the line number
                    id3 = id
                    num = number

            # if id is found which would be put into id3 and is equal to what the user was looking for proceed:
            if id3 == id:

                # Display that the customer ID was found
                print("Customer ID: ", id3, " was found")

                # Initialize variable
                age2 = ""

                # Decrement the line number from the file by 1 and search through the file until this number to find the age (because age is 1 line behind the customerID details)
                num = num - 1
                with open('customers.txt') as f:
                    for i, line in enumerate(f, 1):
                        if i == num:
                            break
                age2 = line

                # Take the digit out of the age2 string
                for word in age2.split():
                        if word.isdigit():
                            age2 = word

                # Set the variables back to their default value, signal to be 0 to indicate that we are creating an account and not opening it
                signal = 0
                index = 0
                num = 0

                # If the user wants to create a savings account do the following:
                if acc_type == 's':
                    # If their age found from using their customer ID is not greater than 14 then they are not allowed to create this type of account (display this to the user), otherwise if they are older than 14, they are allowed to create this type of account

                    if (int(age2) > 14):

                        # Pass their account details to the savings account class and display to the user that their account has been successfully created, set error_checking to 1 so the user can withdraw, deposit, transfer money
                        acc_type = "Savings Account"
                        acc1 = SavingsAcc(IBAN, accNo,funds, signal, num, id, acc_type)
                        print("Your account have been successfully created")
                        error_checking = 1

                    else:
                        print("You need to be at least 14 to create a savings account ")

                        # continue back to the menu
                        continue

                # else if the user wants to create a checking account do the following:
                elif acc_type == 'c':

                    # If their age found from using their customer ID is not greater than 14 then they are not allowed to create this type of account (display this to the user), otherwise if they are older than 14, they are allowed to create this type of account
                    if (int(age2) > 18):

                         # Pass their account details to the checking account class and display to the user that their account has been successfully created, set error_checking to 1 so the user can withdraw, deposit, transfer money
                        acc_type = "Checking Account"
                        acc1 = CheckingAcc(IBAN, accNo,funds, signal, num, id, acc_type)
                        error_checking = 1
                        print("Your account have been successfully created")

                    else:
                        print("You need to be at least 18 to create a checking account")

                        # continue back to the menu
                        continue
                # if the user did not enter 's' or 'c' to create a specified account, display this to the user
                else:
                    print("That's not a valid account type, please enter 's' or 'c' next time.")

            # else the user did not enter an ID found in the customer details file and display the default value error message of id3 to the user
            else:
                print(id3)

    # if operation 2 was entered into the menu do the following:
    elif i == 2:

        # if account was already made or opened do the following:
        if error_checking == 1:

            # Ask user what amount they would like to deposit into their account
            sum = int(input("Amount to be deposited: \n"))

            # Use the deposit method
            acc1.deposit(sum)

        # If account wasn't already made or opened do the following:
        else:

            # Display this to the user
            print("\n** ERROR - Please open account or create account first before depositing **\n")

    # if operation 3 was entered into the menu do the following:
    elif i == 3:

        # if account was already made or opened do the following:
        if error_checking == 1:

            # Ask user what amount they would like to withdraw from their account
            sum = int(input("Amount to be withdrawed: \n"))

            # Use the withdraw method
            acc1.withdraw(sum)

        # If account wasn't already made or opened do the following:
        else:

            # Display this to the user
            print("\n** ERROR - Please open account or create account first before withdrawing **\n")

    # if operation 4 was entered into the menu do the following:
    elif i == 4:

        # Initialize variables and ask user what their account number is to look through the accounts file
        accNumber2 = ""
        accNumber = str(input("Please enter your account number:"))

        # Read the accounts.txt file
        f = open("accounts.txt", "r")
        index = 0
        index2 = 0

        # Find what number the account number line is at and set accNumber2 to be accNumber if the accNumber was found
        for number, line in enumerate(f):
            index += 1

            if accNumber in line:
                accNumber2 = accNumber
                num = number

        # If these do not have the same value when iterating through the loop, then the account number was not found, display this to the user
        if accNumber2 != accNumber:
            print("Unable to retrieve account")

        # Else they do have the same value, so the account number was found and an appropriate message is displayed to the user
        else:
            print("Found account: ", accNumber2)

            # Increment the line number where account number was by 2 to find the funds string value
            num = num + 2

            # set this particular line count for later use
            num2 = num

            # Iterate through the file where the line number is equal to 1 to and put the line value into funds get the funds string value
            with open('accounts.txt') as f:
                for i, line in enumerate(f, 1):
                    if i == num:
                        break
            funds = line

            # Decrement the value of num by 2 to go 2 lines back and iterate through the loop to find the IBAN value
            num2 = num2 - 2
            with open('accounts.txt') as f:
                for i, line in enumerate(f, 1):
                    if i == num2:
                        break
            IBAN = line

            # Increment another 3 lines and iterate through the file again to find the account type of the account
            num2 = num2 +3
            with open('accounts.txt') as f:
                for i, line in enumerate(f, 1):
                    if i == num2:
                        break
            accounttype = line
            accounttype = str(accounttype)

            # Set signal to 1 so when we are outputting to the files in the account class, it updates the values of the account found rather than appending it onto the string again
            signal = 1

            # Grab the integer value from the funds string
            funds = ''.join(x for x in funds if x.isdigit())

            # If the account type of the account found is savings account, enter the savings account subclass
            if (accounttype == "Savings Account"):

                acc1 = SavingsAcc(IBAN, accNumber2,funds, signal, num, id, accounttype)

            # Else the account type of the account found is checking account, enter the checking account subclass
            else:
                acc1 = CheckingAcc(IBAN, accNumber2, funds, signal, num, id, accounttype)

            print(acc1)

            # Set error checking to one so now that the user opened an account, they can now deposit, withdraw, transfer money.
            error_checking = 1

    # if operation 5 was entered into the menu do the following:
    elif i == 5:

        # Ask user to enter their new customer details
        print('Please enter your details below ')
        new_cust_name = input('Name: ')
        new_cust_age = int(input('Age: '))
        new_cust_address = input('Address: ')

        # Pass their account details to the customer account class and put returned value into cust if we need to print the customer details
        cust = Customer(id, new_cust_name, new_cust_age, new_cust_address)


    # if operation 6 was entered into the menu do the following:
    elif i == 6:

        # If account was already opened or created do the following:
        if error_checking == 1:

            # Ask user what amount they would like to transfer from their account
            sum = int(input("Amount to be transferred: \n"))

            # Ask user what IBAN they would like to the transfer money to
            accNumber = str(input("Please enter their IBAN:"))

            # Use transfer method to transfer money
            acc1.transfer(sum, accNumber)

        # If account wasn't already opened or created display an appropriate message
        else:
            print("\n** ERROR - Please open account or create account first before depositing **\n")

     # if operation 8 was entered into the menu do the following:
    elif i == 8:

        # Help used to display docstrings and the class help of the account
        help(Account)

    # if operation outside 1-8 was entered display appropriate error message
    elif i < 1 or i > 8:
        print("Invalid operation please select an option from 1-8")

# If account was opened or created display the account details
if error_checking == 1:
    print("Thank you for using our bank")
    print(acc1)

# Else an account wasnt created or opened so just display goodbye message
else:
    print("Thank you for using our bank")
