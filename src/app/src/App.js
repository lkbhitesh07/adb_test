import './App.css';
import React, {useState, useEffect} from 'react';

const API_BASE_URL = 'http://localhost:8000/todos/';

export function App() {
  // State variables for todo, error message, and the list of todos
  const [todoVal, setTodoVal] = useState('');
  const [allTodos, setAllTodos] = useState([]);
  const [errorMessage, setErrorMessage] = useState(null);

  // Fetch initial todos from the API when the component mounts
  useEffect(async () => {
    const response = await fetch(API_BASE_URL, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const result = await response.json();
      setAllTodos(result.todo_data);
  }, []);

  // Handler for input change
  const handleTodo = (e) => {
    setTodoVal(e.target.value);
  };

  // Handler for submitting a new todo
  const handleSubmit = async (e) => {
    try {
      e.preventDefault();
      const todoRequestBody = { todo: todoVal };
      const response = await fetch(API_BASE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(todoRequestBody),
      });

      if (response.ok) {
        const data = await response.json();
        setAllTodos([...allTodos, data.data]);
        setTodoVal('');
      } else {
        const data = await response.json();
        setErrorMessage(data.message);
      }
    } catch (error) {
      setErrorMessage('An error occurred. Please try again.');
    }
  };

  return (
    <div className="App">
      <div>
        <h1>Create a ToDo</h1>
        <form>
          <div>
            <label for="todo">ToDo: </label>
            <input type="text" value={todoVal} onChange={(e)=>{handleTodo(e)}}/>
          </div>
          <div style={{"marginTop": "5px"}}>
            <button onClick={(e) => {handleSubmit(e)}}>Add ToDo!</button>
          </div>
        </form>
      </div>
      <div>
        <h1>List of ToDos</h1>
        {errorMessage && <p style={{"color": "red"}}>Error: {errorMessage}</p>}
        {allTodos.map((todo, index) => (
          <li key={index}>{todo}</li>
        ))}
      </div>
    </div>
  );
}

export default App;
