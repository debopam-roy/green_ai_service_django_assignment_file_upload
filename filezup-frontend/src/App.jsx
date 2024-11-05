import { React } from 'react';
import {
    BrowserRouter as Router,
    Routes,
    Route,
    useNavigate,
} from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import HomePage from './pages/HomePage';
import { Toaster } from 'react-hot-toast';

const App = () => {
    return (
        <>
            <div>
                <Toaster position="top-right" />
            </div>
            <Router>
                <Routes>
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/" element={<HomePage />} />
                </Routes>
            </Router>
        </>
    );
};

export default App;
