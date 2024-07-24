import streamlit as st
import warnings
import SearchEngine as SE
warnings.filterwarnings("ignore")
import csv
import os
import pandas as pd

def load_data():
    books_df = pd.read_csv('goodbooks-10k/books_cleaned.csv')
    to_read_df = pd.read_csv('goodbooks-10k/to_read.csv')
    favourite_df = pd.read_csv('goodbooks-10k/favourite.csv')
    
    # Rename columns to ensure consistency
    if 'user_id' in to_read_df.columns:
        to_read_df = to_read_df.rename(columns={'user_id': 'User_Id', 'book_id': 'Book_Id'})
    if 'user_id' in favourite_df.columns:
        favourite_df = favourite_df.rename(columns={'user_id': 'User_Id', 'book_id': 'Book_Id'})
    if 'book_id' in books_df.columns:
        books_df = books_df.rename(columns={'book_id': 'Book_Id'})
    
    print("Books columns:", books_df.columns)
    print("To-read columns:", to_read_df.columns)
    print("Favourite columns:", favourite_df.columns)
    
    return books_df, to_read_df, favourite_df

def save_to_read(user_id, book_id):
    with open('goodbooks-10k/to_read.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, book_id])

def save_favourite(user_id, book_id):
    filename = 'goodbooks-10k/favourite.csv'
    if not os.path.isfile(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['User_Id', 'Book_Id'])
    
    df = pd.read_csv(filename)
    if not ((df['User_Id'] == user_id) & (df['Book_Id'] == book_id)).any():
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_id, book_id])
        return True
    return False

def get_available_columns(df, desired_columns):
    return [col for col in desired_columns if col in df.columns]

def main():
    st.title("Personalized Book Search Engine")

    books_df, to_read_df, favourite_df = load_data()

    decision = st.radio("What would you like to do?", 
                        ("Book Search", "View Wishlist/To-Read List"))

    user_id = st.number_input("Enter User ID (0-53424)", min_value=0, max_value=53424)

    if decision == "Book Search":
        search_eng = SE.SearchEngine()
        query = st.text_input("Enter your text/query to find similar recommendations")
        boosting_factor = st.slider("Enter to_read_boosting_factor", 0.0, 10.0, 1.0)
        top_recommenders = st.slider("Number of Top Recommendations", 1, 50, 10)

        if st.button("Search"):
            with st.spinner("Searching..."):
                res = search_eng.query(user_id=user_id, text=query, 
                                       to_read_boosting_factor=boosting_factor, 
                                       K=top_recommenders, save_res=True)
            st.write(res)
            st.success("Results saved locally.")

        action = st.radio("Additional Actions", 
                          ("Add to To-Read List", "Add to Favourites", "View Favourites", "None"))

        if action == "Add to To-Read List":
            book_id = st.number_input("Enter Book ID to add to To-Read list", min_value=0)
            if st.button("Add to To-Read"):
                save_to_read(user_id, book_id)
                st.success("Book added to To-Read list!")

        elif action == "Add to Favourites":
            book_id = st.number_input("Enter Book ID to add to Favourites", min_value=0)
            if st.button("Add to Favourites"):
                if save_favourite(user_id, book_id):
                    st.success("Book added to Favourites!")
                else:
                    st.info("This book is already in your Favourites.")

        elif action == "View Favourites":
            user_id = st.input("Enter User ID (0-53424)")
            if st.button("View Favourites"):
                user_favourites = favourite_df[favourite_df['User_Id'] == user_id]
                if not user_favourites.empty:
                    favourite_books = books_df[books_df['Book_Id'].isin(user_favourites['Book_Id'])]
                    columns_to_display = get_available_columns(favourite_books, ['Book_Id', 'Author', 'Title', 'isbn13'])
                    st.write(favourite_books[columns_to_display])
                else:
                    st.info("No favourites found for this user.")

    else:  # View Wishlist/To-Read List
        if st.button("View To-Read List"):
            user_to_read = to_read_df[to_read_df['User_Id'] == user_id]
            if not user_to_read.empty:
                to_read_books = books_df[books_df['Book_Id'].isin(user_to_read['Book_Id'])]
                columns_to_display = get_available_columns(to_read_books, ['Book_Id', 'Author', 'Title', 'isbn13'])
                st.write(to_read_books[columns_to_display])
                st.success("Pick any one book and enjoy your reading from your wishlist!")
            else:
                st.info("No books in the To-Read list for this user.")

if __name__ == "__main__":
    main()
