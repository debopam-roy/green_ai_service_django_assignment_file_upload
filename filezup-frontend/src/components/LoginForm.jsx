import React, { useState } from 'react';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom

const LoginForm = ({ formSubmit }) => {
    const [showPassword, setShowPassword] = useState(false);
    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });

    const togglePasswordVisibility = () => {
        setShowPassword(!showPassword);
    };
    const handleSubmission = (e) => {
        e.preventDefault();
        formSubmit(formData);
    };
    return (
        <div
            className="card p-4 bg-light mx-auto"
            style={{
                width: '400px',
                height: 'auto',
                backgroundColor: '#f8f9fa',
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                borderRadius: '10px',
                border: '1px solid #f0f0f0',
            }}
        >
            <div className="card-body text-center">
                <h4 className="card-title">Hello,</h4>
                <p className="card-text">Welcome Back!</p>
            </div>
            <form onSubmit={handleSubmission}>
                {/* username Input */}
                <div className="form-outline mb-4">
                    <label className="form-label" htmlFor="user_name">
                        User Name
                    </label>
                    <input
                        type="text"
                        id="user_name"
                        placeholder="john_doe"
                        className="form-control"
                        onChange={(e) =>
                            setFormData({
                                ...formData,
                                username: e.target.value,
                            })
                        }
                        style={{ borderRadius: '8px', padding: '10px' }}
                    />
                </div>

                {/* Password Input with Eye Icon */}
                <div className="form-outline mb-4 position-relative">
                    <label className="form-label" htmlFor="password">
                        Password
                    </label>
                    <input
                        type={showPassword ? 'text' : 'password'}
                        id="password"
                        className="form-control"
                        placeholder="********"
                        onChange={(e) =>
                            setFormData({
                                ...formData,
                                password: e.target.value,
                            })
                        }
                        style={{ borderRadius: '8px', padding: '10px' }}
                    />
                    <span
                        className="position-absolute"
                        style={{
                            right: '15px',
                            top: '42px',
                            cursor: 'pointer',
                        }}
                        onClick={togglePasswordVisibility}
                    >
                        {showPassword ? <FaEyeSlash /> : <FaEye />}
                    </span>
                </div>

                {/* Sign In Button */}
                <button
                    type="submit"
                    className="btn btn-primary btn-block"
                    style={{
                        width: '100%',
                        borderRadius: '8px',
                        padding: '10px',
                    }}
                >
                    Sign in
                </button>

                {/* Register Link */}
                <div className="text-center mt-3">
                    <p>
                        Not yet a member?{' '}
                        <Link to="/register">Register Here</Link>
                    </p>
                </div>
            </form>
        </div>
    );
};

export default LoginForm;
