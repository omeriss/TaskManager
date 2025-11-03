import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import HomePage from "./pages/HomePage/HomePage";
import NavBar from "./components/NavBar/NavBar";
import About from "./pages/About/About";
import "./styles/global.css";

const App = () => {
  return (
    <BrowserRouter>
      <header>
        <NavBar />
      </header>

      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<About />} />
          <Route
            path="*"
            element={
              <div>
                <h2>Page not found</h2>
                <Link to="/">Go home</Link>.
              </div>
            }
          />
        </Routes>
      </main>
    </BrowserRouter>
  );
};

export default App;
