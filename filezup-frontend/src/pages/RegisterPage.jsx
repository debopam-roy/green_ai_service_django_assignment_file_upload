import React from 'react';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import RegisterForm from '../components/RegisterForm.jsx';
import axios from 'axios';
import { useDispatch } from 'react-redux';

const RegisterPage = () => {
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const handleRegisterPageSubmit = async (formData) => {
        const registerFormData = {
            fullname: formData.fullname,
            username: formData.username,
            email: formData.email,
            password: formData.password,
        };
        try {
            const response = await axios.post(
                `http://127.0.0.1:8000/api/register/`,
                registerFormData,
                {
                    withCredentials: true,
                }
            );
            if (response.status === 201) {
                const { user_id, username, fullname, email, token } =
                    response.data;
                dispatch(
                    addUser({ user_id, username, fullname, email, token })
                );
                //TODO: Proper toast message
                navigate('/');
            } else {
                //TODO: Proper toast message
                console.error('Unexpected response status:', response.status);
            }
        } catch (error) {
            if (error.response) {
                console.error('Response data:', error.response.data); // Inspect the error message here
            }
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
            <RegisterForm formSubmit={handleRegisterPageSubmit} />
        </>
    );
};

export default RegisterPage;
