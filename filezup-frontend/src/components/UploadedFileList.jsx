import React from 'react';
import { MdOutlineDeleteOutline, MdDownload } from 'react-icons/md';
import Lottie from 'lottie-react';
import emptyAnimation from '../assets/empty_content.json';

import pdfIcon from '../assets/pdf.png';
import imageIcon from '../assets/image.png';
import docIcon from '../assets/doc.png';
import svgIcon from '../assets/svg.png';
import defaultIcon from '../assets/file.png';

const fileTypeIcons = {
    pdf: pdfIcon,
    image: imageIcon,
    doc: docIcon,
    svg: svgIcon,
    txt: '../assets/txt.png',
    ppt: '../assets/ppt.png',
    xls: '../assets/xls.png',
    mp4: '../assets/mp4.png',
    mp3: '../assets/mp3.png',
    zip: '../assets/zip.png',
    rar: '../assets/rar.png',
    json: '../assets/json.png',
    csv: '../assets/csv.png',
    markdown: '../assets/md.png',
    xml: '../assets/xml.png',
};

const getFileTypeIcon = (file) => {
    const extension = file.file_name.split('.').pop().toLowerCase();
    return fileTypeIcons[extension] || defaultIcon;
};

const UploadedFileList = ({ files, handleDelete, handleDownload }) => {
    return (
        <div className="uploaded-file-list">
            {files.length > 0 ? (
                <ul className="list-group">
                    {files.map((file) => (
                        <li
                            key={file.id}
                            className="list-group-item d-flex justify-content-between align-items-center"
                            style={{
                                backgroundColor: '#ffffff',
                                borderRadius: '8px',
                                boxShadow: '0 2px 5px rgba(0, 0, 0, 0.1)',
                                marginBottom: '12px',
                                padding: '12px 16px',
                                transition: 'transform 0.2s',
                            }}
                        >
                            <div className="file-info d-flex align-items-center">
                                <img
                                    src={getFileTypeIcon(file)}
                                    alt="File Type Icon"
                                    style={{
                                        borderRadius: '50%',
                                        width: '36px',
                                        height: '36px',
                                        marginRight: '12px',
                                    }}
                                />
                                <span
                                    style={{
                                        fontWeight: '600',
                                        fontSize: '14px',
                                        color: '#333',
                                        maxWidth: '150px',
                                        whiteSpace: 'nowrap',
                                        overflow: 'hidden',
                                        textOverflow: 'ellipsis',
                                    }}
                                >
                                    {file.file_name.split('/').pop()}
                                </span>
                            </div>
                            <div className="action-icons d-flex align-items-center">
                                <MdDownload
                                    onClick={() => handleDownload(file.id)}
                                    style={{
                                        color: '#6EA0FF',
                                        fontSize: '24px',
                                        marginLeft: '8px',
                                        cursor: 'pointer',
                                        transition: 'color 0.3s',
                                    }}
                                    onMouseEnter={(e) =>
                                        (e.currentTarget.style.color =
                                            '#0056b3')
                                    }
                                    onMouseLeave={(e) =>
                                        (e.currentTarget.style.color =
                                            '#007bff')
                                    }
                                />
                                <MdOutlineDeleteOutline
                                    onClick={() => handleDelete(file.id)}
                                    style={{
                                        color: '#dc3545',
                                        fontSize: '24px',
                                        marginLeft: '8px',
                                        cursor: 'pointer',
                                        transition: 'color 0.3s',
                                    }}
                                    onMouseEnter={(e) =>
                                        (e.currentTarget.style.color =
                                            '#c82333')
                                    }
                                    onMouseLeave={(e) =>
                                        (e.currentTarget.style.color =
                                            '#dc3545')
                                    }
                                />
                            </div>
                        </li>
                    ))}
                </ul>
            ) : (
                <div className="text-center">
                    <Lottie
                        animationData={emptyAnimation}
                        loop={true}
                        style={{ maxWidth: '300px', margin: '0 auto' }}
                    />
                    <p
                        style={{
                            color: '#999',
                            fontSize: '16px',
                            marginTop: '16px',
                        }}
                    >
                        No files uploaded yet.
                    </p>
                </div>
            )}
        </div>
    );
};

export default UploadedFileList;
