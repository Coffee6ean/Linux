import { BrowserRouter, Route, RouterProvider, Routes, createBrowserRouter } from "react-router-dom";
import Upload from "./routes/upload";
import Home from "./routes/home";

import './App.css';

const router = createBrowserRouter([
  {path: "/", element: <Home/>},
  {path: "/upload", element: <Upload/>}
])

function App() {
  return (
    <div className="app-container">
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
