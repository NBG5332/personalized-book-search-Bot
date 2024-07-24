print("\n\nWelcom to Personalized Book Search Engine\n\n")


import warnings
import SearchEngine as SE
warnings.filterwarnings("ignore")
import csv
import os
import pandas as pd

decision = input("Enter 1 if you want to proceed to Book Search to find similar books\nEnter 2 if you want to continue with books in your wishlist/to_read \n")
if(decision =='1'):
    search_eng = SE.SearchEngine()
    user_id = int(input("Enter User_Id between 0-53424\n")) # 0-53424
    query = input("Enter your text/query to find similar recommadtions to it.\n")
    save_res =True
    boosting_factor = float(input("Enter to_read_boosting_factor ? :\n"))
    top_recommenders = int(input("Enter number of Top Recomandation you want see?\n"))
    if __name__ == "__main__":
        print("On My Way...... 🏋️ 💬 W🕛RK🏋️ ING 🕡N🏋️ IT✅")
        res = search_eng.query(user_id=user_id, text=query,to_read_boosting_factor = boosting_factor, K=top_recommenders, save_res=save_res)
        print(res)
        if save_res:
            print("Results saved to local.")
        else:
            print("Complete")

    x = input("enter 1 if you want to add book in to_read list for future perpose's\nenter 2 if you want to add any book into your Favourite List\nenter 3 if you want to see user Favourite list of books\nIf not enter any key😊😊\n")
    if(x=='1'):
        # Open the CSV file in append mode
        with open('/Users/cdmstudent/Desktop/DSC-540 Adv ML/Final Project/ChatBot/PersonalizedBookSearchgoodbooks-10k/to_read.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            book_id = input("enter book_id: ")
            #user_id = input("enter user_id: ")
            # Create a new row as a list or tuple
            new_row = [user_id,book_id]

            # Write the new row to the CSV file
            writer.writerow(new_row)

    if(x=='2'):
        filename = '/Users/cdmstudent/Desktop/DSC-540 Adv ML/Final Project/ChatBot/PersonalizedBookSearch/goodbooks-10k/favourite.csv'

        # Create a new CSV file with headers for two columns User_Id & Book_Id if it doesn't exist
        if not os.path.isfile(filename):
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['User_Id', 'Book_Id'])  # Write headers for the two columns

        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            book_id = input("enter book_id: ")
            #user_id = input("enter user_id: ")
            i =1
            for row in reader:
                if user_id in row and book_id in row:
                    print("Entered User_Id had this book in the Favourite List")
                    i = 0
                    break
                else: continue
        if(i==1):
            # Open the CSV file in append mode
            with open(filename, mode='a', newline='') as file:
                print("Entered User_Id & Book_Id not in your Favourite List, Now we are going to add into it.") 
                writer = csv.writer(file)
                new_row = [user_id,book_id]

                # Write the new row to the CSV file
                writer.writerow(new_row)

    if(x=='3'):
        # open the CSV file
        with open('/Users/cdmstudent/Desktop/DSC-540 Adv ML/Final Project/ChatBot/PersonalizedBookSearch/goodbooks-10k/favourite.csv', 'r') as file:

            # create a CSV reader object
            reader = csv.reader(file)

            # read the header row
            header = next(reader)

            # create an empty list to store matching rows
            matching_rows = []

            # get the user input
            entered_value = input('Enter User_Id to search: ')

            # loop through the rows and check for matches
            for row in reader:
                if entered_value == row[0]:
                    with open('/Users/cdmstudent/Desktop/DSC-540 Adv ML/Final Project/ChatBot/PersonalizedBookSearch/goodbooks-10k/books_cleaned.csv', 'r') as file1:
                        reader1 = csv.reader(file1)
                        header = next(reader1)
                        for row1 in reader1:
                            if row[1] == row1[0]:
                                matching_rows.append(row1)

        print(pd.DataFrame(matching_rows, columns = ['Book_id','Author','Title','isbn13']))


    else: print("Thank You for using Personalized Book Search Engine")
    

if(decision=='2'):
    # open the CSV file
    with open('/Users/cdmstudent/Desktop/DSC-540 Adv ML/Final Project/ChatBot/PersonalizedBookSearch/goodbooks-10k/to_read.csv', 'r') as file:

        # create a CSV reader object
        reader = csv.reader(file)

        # read the header row
        header = next(reader)

        # create an empty list to store matching rows
        matching_rows = []

        # get the user input
        entered_value = input('Enter User_id to search: ')

        # loop through the rows and check for matches
        for row in reader:
            if entered_value == row[0]:

                with open('/Users/cdmstudent/Desktop/DSC-540 Adv ML/Final Project/ChatBot/PersonalizedBookSearch/goodbooks-10k/books_cleaned.csv', 'r') as file1:
                    reader1 = csv.reader(file1)
                    header = next(reader1)
                    for row1 in reader1:
                        if row[1] == row1[0]:
                            matching_rows.append(row1)

    print(pd.DataFrame(matching_rows, columns = ['Book_id','Author','Title','isbn13']))
    print("\nPick anyone one book and enjoy your reading with whishlist books")

if(decision!='2' and decision !='1'and decision== True): print("Typo error, please type 1 or 2 according to your plan\nThank you😊😊")