import React, { useState } from 'react';
import './bookFormStyle.css';

const BookForm = (props) => {
  const [title, setTitle] = useState("")
  const [author, setAuthor] = useState("")
  const [description, setDescription] = useState("")
  const [errorMessage, setErrorMessage] = useState(null)
  const [previousSelectedBook, setPreviousSelectedBook] = useState(null)

  if (props.selectedBook && (props.selectedBook !== previousSelectedBook)) {
    setPreviousSelectedBook(props.selectedBook)
    setTitle(props.selectedBook.title)
    setAuthor(props.selectedBook.author)
    setDescription(props.selectedBook.description)
    setErrorMessage("")
  }

  const clearForm = () => {
    setTitle("")
    setAuthor("")
    setDescription("")
  }

  const validateForm = () => {
    if (title !== "" && author !== "" && description !== "") {
      return true
    } else {
      setErrorMessage("Error: Missing fields")
      return false
    }
  }

  const saveNewBook = (event) => { 
    event.preventDefault()
    if (validateForm()) {
      const book = { title, author, description }
      fetch("api/books/", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify(book)
      })
      .then((response) => props.callUpdateBookList(response))
      clearForm()
      props.callSetSelectedBook(null)
    }
  }

  const updateBook = (event) => { 
    event.preventDefault()
    if (validateForm()) {
      const book = { title, author, description }
      fetch("api/books/" + props.selectedBook.book_id + "/", {
        method: "PUT",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify(book)
      })
      .then((response) => props.callUpdateBookList(response))
    }
  }

  const deleteBook = (event) => {
    event.preventDefault()

    fetch("api/books/" + props.selectedBook.book_id + "/", {
      method: "DELETE",
      headers: { "Content-Type": "application/json"},
    })
    .then((response) => props.callUpdateBookList(response))
    clearForm()
    props.callSetSelectedBook(null)
  }

  return (
    <form>
      <label htmlFor="title">Title:</label>
      <input
        type="text"
        id="title"
        value={title}
        onChange={(e) => {
          setTitle(e.target.value);
          setErrorMessage("")}
        }
      />

      <label htmlFor="author">Author:</label>
      <input
        type="text"
        id="author"
        value={author}
        onChange={(e) => {
          setAuthor(e.target.value);
          setErrorMessage("")}
        }
      />

      <label htmlFor="description">Description:</label>
      <textarea
        id="description"
        value={description}
        onChange={(e) => {
          setDescription(e.target.value);
          setErrorMessage("")}
        }
      />

      <button onClick={(e) => saveNewBook(e)}>
          Save New</button>

      <button onClick={(e) => updateBook(e)}
          disabled={!props.selectedBook}>
          Save</button>

      <button onClick={(e) => deleteBook(e)}
          disabled={!props.selectedBook}>
          Delete</button>

      <p className="errorMessage">{errorMessage}</p>
    </form>
  )
}

export default BookForm;

