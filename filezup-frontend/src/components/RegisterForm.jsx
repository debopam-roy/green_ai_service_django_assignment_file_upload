import React, { useState } from 'react';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import { Link } from 'react-router-dom';

const RegisterForm = ({ formSubmit }) => {
    const [showPassword, setShowPassword] = useState(false);
    const [formData, setFormData] = useState({
        fullname: '',
        username: '',
        email: '',
        password: '',
    });

    const togglePasswordVisibility = () => {
        setShowPassword(!showPassword);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        formSubmit(formData);
    };

    return (
        <div
            className="card p-4 mx-auto"
            style={{
                width: '400px',
                backgroundColor: '#f8f9fa',
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                borderRadius: '10px',
                border: '1px solid #f0f0f0',
            }}
        >
            <div className="card-body text-center">
                <h4 className="card-title">Welcome,</h4>
                <p className="card-text">Create Your Account</p>
            </div>
            <form onSubmit={handleSubmit}>
                {/* Full Name Input */}
                <div className="form-outline mb-4">
                    <label className="form-label" htmlFor="fullname">
                        Full Name
                    </label>
                    <input
                        type="text"
                        id="fullname"
                        placeholder="John Doe"
                        className="form-control"
                        value={formData.fullname}
                        onChange={(e) =>
                            setFormData({
                                ...formData,
                                fullname: e.target.value,
                            })
                        }
                        style={{ borderRadius: '8px', padding: '10px' }}
                        required
                    />
                </div>

                {/* Username Input */}
                <div className="form-outline mb-4">
                    <label className="form-label" htmlFor="username">
                        User Name
                    </label>
                    <input
                        type="text"
                        id="username"
                        placeholder="john_doe"
                        className="form-control"
                        value={formData.username}
                        onChange={(e) =>
                            setFormData({
                                ...formData,
                                username: e.target.value,
                            })
                        }
                        style={{ borderRadius: '8px', padding: '10px' }}
                        required
                    />
                </div>

                {/* Email Input */}
                <div className="form-outline mb-4">
                    <label className="form-label" htmlFor="email">
                        Email
                    </label>
                    <input
                        type="email"
                        id="email"
                        placeholder="email@example.com"
                        className="form-control"
                        value={formData.email}
                        onChange={(e) =>
                            setFormData({ ...formData, email: e.target.value })
                        }
                        style={{ borderRadius: '8px', padding: '10px' }}
                        required
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
                        value={formData.password}
                        onChange={(e) =>
                            setFormData({
                                ...formData,
                                password: e.target.value,
                            })
                        }
                        style={{ borderRadius: '8px', padding: '10px' }}
                        required
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

                {/* Register Button */}
                <button
                    type="submit"
                    className="btn btn-primary btn-block"
                    style={{
                        width: '100%',
                        borderRadius: '8px',
                        padding: '10px',
                    }}
                >
                    Register
                </button>

                {/* Login Link */}
                <div className="text-center mt-3">
                    <p>
                        Already have an account?{' '}
                        <Link to="/login">Login Here</Link>
                    </p>
                </div>
            </form>
        </div>
    );
};

export default RegisterForm;
