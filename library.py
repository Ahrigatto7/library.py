import streamlit as st
import json
import os

# File to save and load the library
LIBRARY_FILE = "library.json"

# Load library from file if it exists
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, 'r') as f:
            return json.load(f)
    return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, 'w') as f:
        json.dump(library, f, indent=4)

# Display a single book
def display_book(book):
    read_status = "✅ Read" if book["Read"] else "📖 Unread"
    st.write(f"**{book['Title']}** by *{book['Author']}* ({book['Year']}) - {book['Genre']} [{read_status}]")

# App starts here
def main():
    st.title("📚 Personal Library Manager")

    library = load_library()

    menu = ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add a Book":
        st.subheader("Add a New Book")
        with st.form("add_book_form"):
            title = st.text_input("Title")
            author = st.text_input("Author")
            year = st.number_input("Publication Year", min_value=0, step=1)
            genre = st.text_input("Genre")
            read = st.radio("Read Status", ["Unread", "Read"])
            submitted = st.form_submit_button("Add Book")

            if submitted:
                book = {
                    "Title": title,
                    "Author": author,
                    "Year": int(year),
                    "Genre": genre,
                    "Read": True if read == "Read" else False
                }
                library.append(book)
                save_library(library)
                st.success(f"Book '{title}' added!")

    elif choice == "Remove a Book":
        st.subheader("Remove a Book")
        titles = [book["Title"] for book in library]
        if titles:
            book_to_remove = st.selectbox("Select a book to remove", titles)
            if st.button("Remove Book"):
                library = [book for book in library if book["Title"] != book_to_remove]
                save_library(library)
                st.success(f"Book '{book_to_remove}' removed!")
        else:
            st.info("No books to remove.")

    elif choice == "Search for a Book":
        st.subheader("Search Books")
        query = st.text_input("Search by title or author")
        if query:
            results = [book for book in library if query.lower() in book["Title"].lower() or query.lower() in book["Author"].lower()]
            if results:
                for book in results:
                    display_book(book)
            else:
                st.warning("No matching books found.")

    elif choice == "Display All Books":
        st.subheader("All Books in Library")
        if library:
            for book in library:
                display_book(book)
        else:
            st.info("Library is empty.")

    elif choice == "Display Statistics":
        st.subheader("Library Statistics")
        total_books = len(library)
        if total_books == 0:
            st.info("No books in the library.")
        else:
            read_books = sum(1 for book in library if book["Read"])
            percentage_read = (read_books / total_books) * 100
            st.metric("Total Books", total_books)
            st.metric("Books Read", f"{read_books} ({percentage_read:.2f}%)")

if __name__ == "__main__":
    main()
