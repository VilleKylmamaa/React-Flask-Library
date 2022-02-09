import React, { useState, useEffect } from 'react';
import BookList from './Components/BookList';
import BookForm from './Components/BookForm';
import './App.css';

function App() {
  const [databaseBooks, setBooks] = useState([]);
  const [selectedBook, setSelectedBook] = useState(null);
  
  useEffect(() => {
    updateBookList()
  }, []);

  const updateBookList = () => {
    fetch("/api/books/")
      .then(response => response.json())
      .then(data => { setBooks(data.items) })
  }

  return (
    <div className="App">
      <div className="App-header">Library</div>
      <section>
        <div className="row">

          <div className="column">
            <BookForm 
              callSetSelectedBook={setSelectedBook}
              callUpdateBookList={updateBookList}
              selectedBook={selectedBook}
            />
          </div>

          <div className="column">
            <BookList
              callSetSelectedBook={setSelectedBook}
              selectedBook={selectedBook}
              books={databaseBooks}
            />
          </div>

        </div>
      </section>
    </div>
  );
}

export default App;
