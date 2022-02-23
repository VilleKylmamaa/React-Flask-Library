import React from 'react';
import './bookListStyle.css';

const BookList = (props) => {
  if (props.books.length > 0) {
    return (
      <div className="bookList">
      {props.books && props.books.map(book =>{
        return (
          <div 
            className={
              // Only the selected book has active class
              props.selectedBook && (book.book_id === props.selectedBook.book_id)
              ? 'active bookItem' : 'bookItem'
            }
            onClick={() => {props.callSetSelectedBook(book);}}
            key={ book.book_id }
          >
            <h2 className="bookTitle"> { book.title} </h2>
            <p className="bookAuthor"> { book.author } </p>
          </div>
        )
        })}
      </div>
    )
  } else {
    return null
  }
}

export default BookList;

