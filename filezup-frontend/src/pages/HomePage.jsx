import React, { useEffect, useState } from 'react';
import { AiOutlineLogout } from 'react-icons/ai';
import { useDispatch } from 'react-redux';
import { removeUser } from '../features/authentication/authenticationSlices.js';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { MdOutlineDeleteOutline } from 'react-icons/md';
import UploadedFileList from '../components/UploadedFileList.jsx';
import FilePicker from '../components/FilePicker.jsx';

const HomePage = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [userData, setUserData] = useState({});
    const [files, setFiles] = useState([]);
    const [uploadingFiles, setUploadingFiles] = useState([]);
    const [greeting, setGreeting] = useState('');

    const handleLogout = async () => {
        try {
            const response = await axios.post(
                `http://127.0.0.1:8000/api/logout/${userData.username}/`,
                {},
                {
                    headers: {
                        Authorization: `Bearer ${userData.token}`,
                    },
                    withCredentials: true,
                }
            );
            if (response.status === 200) {
                dispatch(removeUser());
                navigate('/login');
            } else {
                console.error('Unexpected response status:', response.status);
            }
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    const handleFileChange = (event) => {
        const selectedFiles = Array.from(event.target.files);
        setUploadingFiles(selectedFiles);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        uploadingFiles.forEach((file) => {
            formData.append('file', file);
        });

        try {
            const response = await axios.post(
                'http://127.0.0.1:8000/api/file/upload/',
                formData,
                {
                    headers: {
                        Authorization: `Bearer ${userData.token}`,
                        'Content-Type': 'multipart/form-data',
                    },
                    withCredentials: true,
                }
            );
            if (response.status === 200) {
                fetchFiles();
                setUploadingFiles([]);
                //when calling upto this line, I want the list to be automatically parsed again so that the list gets updated in the ui automatically
            }
        } catch (error) {
            console.error('File upload failed:', error);
        }
    };

    const fetchFiles = async (token) => {
        try {
            const response = await axios.get(
                'http://127.0.0.1:8000/api/file/',
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                    withCredentials: true,
                }
            );
            console.log(response.data);
            setFiles(response.data);
            //when calling upto this line, I want the list to be automatically parsed again so that the list gets updated in the ui automatically
        } catch (error) {
            console.error('Failed to fetch files:', error);
        }
    };

    const handleDelete = async (fileId) => {
        try {
            const response = await axios.delete(
                `http://127.0.0.1:8000/api/file/delete/${fileId}/`,
                {
                    headers: {
                        Authorization: `Bearer ${userData.token}`,
                    },
                    withCredentials: true,
                }
            );
            if (response.status === 204) {
                fetchFiles();
                //when calling upto this line, I want the list to be automatically parsed again so that the list gets updated in the ui automatically
            }
        } catch (error) {
            console.error('File deletion failed:', error);
        }
    };

    const handleDownload = async (fileId) => {
        try {
            const response = await axios.get(
                `http://127.0.0.1:8000/api/file/download/${fileId}/`,
                {
                    headers: {
                        Authorization: `Bearer ${userData.token}`,
                    },
                    responseType: 'blob',
                    withCredentials: true,
                }
            );

            if (response.status === 200) {
                // Get the original filename from response headers
                const originalFilename = response.headers['content-disposition']
                    ? response.headers['content-disposition']
                          .split('filename=')[1]
                          .replace(/"/g, '')
                    : `downloaded_file_${fileId}`; // Fallback if no filename is found

                const url = window.URL.createObjectURL(
                    new Blob([response.data])
                );
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', originalFilename); // Use the original filename
                document.body.appendChild(link);
                link.click();
                link.remove(); // Clean up the link after triggering the download
                fetchFiles(); // Refresh the file list after download
            }
        } catch (error) {
            console.error('File download failed:', error);
            alert('Failed to download the file. Please try again.'); // User-friendly error message
        }
    };

    useEffect(() => {
        const user_details = JSON.parse(
            localStorage.getItem('userAuthentication')
        );

        if (!user_details || !user_details.is_authenticated) {
            navigate('/login');
            return;
        }
        setUserData(user_details);
        fetchFiles(user_details.token);

        const currentHour = new Date().getHours();
        if (currentHour < 12) {
            setGreeting('Good morning');
        } else if (currentHour < 18) {
            setGreeting('Good afternoon');
        } else {
            setGreeting('Good evening');
        }
        //when calling upto this line, I want the list to be automatically parsed again so that the list gets updated in the ui automatically
    }, [navigate]);

    return (
        <div className="container">
            <div
                className="top-bar d-flex justify-content-between align-items-center p-4"
                style={{
                    backgroundColor: '#6EA0FF',
                    color: '#fff',
                    borderRadius: '10px',
                    boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
                }}
            >
                <h1 className="mb-0" style={{ fontFamily: 'sans' }}>
                    {greeting}, {userData.fullname}.
                </h1>
                <AiOutlineLogout
                    style={{
                        fontSize: '30px',
                        color: '#dc3545',
                        cursor: 'pointer',
                    }}
                    onClick={handleLogout}
                />
            </div>

            <div className="row mt-4">
                <div
                    className="col-lg-6 col-md-12 mb-4 d-flex flex-column align-items-center justify-content-center mx-1" // Added mx-1 for horizontal margin
                    style={{
                        backgroundColor: '#fff',
                        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
                        borderRadius: '10px',
                        border: '1px solid #f0f0f0',
                        padding: '20px',
                        flex: 1,
                    }}
                >
                    <h3>Upload File(s)</h3>
                    <FilePicker
                        handleFileChange={handleFileChange}
                        handleUpload={handleUpload}
                        uploadingFiles={uploadingFiles}
                    />

                    <ul className="list-group mt-3" style={{ width: '100%' }}>
                        {uploadingFiles.length > 0 ? (
                            uploadingFiles.map((file, index) => (
                                <li
                                    key={index}
                                    className="list-group-item d-flex justify-content-between align-items-center"
                                    style={{
                                        borderRadius: '5px',
                                        backgroundColor: '#f8f9fa',
                                        boxShadow:
                                            '0 1px 4px rgba(0, 0, 0, 0.1)',
                                        marginBottom: '10px',
                                    }}
                                >
                                    {file.name}

                                    <MdOutlineDeleteOutline
                                        style={{
                                            color: 'red',
                                            fontSize: '28px',
                                            cursor: 'pointer',
                                            transition: 'all 0.3s ease',
                                            borderRadius: '50%',
                                            padding: '4px',
                                        }}
                                        onMouseEnter={(e) => {
                                            e.currentTarget.style.backgroundColor =
                                                'rgba(255, 0, 0, 0.1)';
                                        }}
                                        onMouseLeave={(e) => {
                                            e.currentTarget.style.backgroundColor =
                                                'transparent';
                                        }}
                                        onClick={() =>
                                            setUploadingFiles(
                                                uploadingFiles.filter(
                                                    (_, i) => i !== index
                                                )
                                            )
                                        }
                                    />
                                </li>
                            ))
                        ) : (
                            <li
                                className="list-group-item"
                                style={{ border: '0.px solid' }}
                            >
                                No files selected
                            </li>
                        )}
                    </ul>
                </div>

                <div
                    className="col-lg-6 col-md-12 mb-4 d-flex flex-column align-items-center justify-content-center mx-1" // Added mx-1 for horizontal margin
                    style={{
                        backgroundColor: '#fff',
                        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
                        borderRadius: '10px',
                        border: '1px solid #f0f0f0',
                        padding: '20px',
                        flex: 1,
                    }}
                >
                    <h3>Uploaded Files</h3>
                    <UploadedFileList
                        files={files}
                        handleDelete={handleDelete}
                        handleDownload={handleDownload}
                    />
                </div>
            </div>
        </div>
    );
};

export default HomePage;