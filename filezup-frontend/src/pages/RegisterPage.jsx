import React from 'react';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import RegisterForm from '../components/RegisterForm.jsx';
import axios from 'axios';
import { toast } from 'react-hot-toast';

const RegisterPage = () => {
    const navigate = useNavigate();
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
                registerFormData
            );

            if (response.status === 201) {
                toast.success(
                    'Registration successful. Please login to your account.'
                );
                navigate('/login');
            } else {
                toast.error('Unexpected response status:', response.status);
            }
        } catch (error) {
            if (error.response) {
                toast.error(
                    'Error occured. Response data:',
                    error.response.data
                );
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
