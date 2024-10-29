import React from 'react';
import { useEffect } from 'react';
import LoginForm from '../components/LoginForm';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { addUser } from '../features/authentication/authenticationSlices';
import { toast } from 'react-hot-toast';

const LoginPage = () => {
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const handleLoginPageSubmit = async (formData) => {
        const loginFormData = {
            username: formData.username,
            password: formData.password,
        };
        const response = await axios.post(
            `http://127.0.0.1:8000/api/login/`,
            loginFormData,
            { withCredentials: true }
        );

        if (response.status === 200) {
            const { user_id, username, fullname, email, token } = response.data;
            dispatch(addUser({ user_id, username, fullname, email, token }));
            toast.success('Registration successful');
            navigate('/');
        } else {
            toast.success(`Oops! Error occured.${response.status}`);
        }
    };

    useEffect(() => {
        const user_details = JSON.parse(
            localStorage.getItem('userAuthentication')
        );
        if (user_details && user_details.is_authenticated) {
            navigate('/');
            return;
        }
    }, []);

    return (
        <>
            <LoginForm formSubmit={handleLoginPageSubmit} />
        </>
    );
};

export default LoginPage;
