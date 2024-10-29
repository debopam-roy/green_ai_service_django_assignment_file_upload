import React from 'react';

const FilePicker = ({ handleFileChange, handleUpload, uploadingFiles }) => {
    return (
        <div className="file-upload-container" style={styles.container}>
            <input
                type="file"
                multiple
                onChange={handleFileChange}
                className="form-control-file"
                style={styles.fileInput}
            />
            <button
                className="btn btn-primary w-100"
                onClick={handleUpload}
                disabled={uploadingFiles.length === 0}
                style={styles.uploadButton}
            >
                Upload
            </button>
        </div>
    );
};

const styles = {
    container: {
        border: '1px dashed ', // Dotted border style
        borderRadius: '5px',
        padding: '20px',
        margin: '20px 0',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center', // Center align items
        justifyContent: 'center',
        transition: 'box-shadow 0.3s',
    },
    fileInput: {
        borderRadius: '5px',
        border: '1px dotted',
        padding: '10px',
        width: '100%', // Ensure full width for the input
        marginBottom: '15px',
        outline: 'none', // Remove outline for focus
        transition: 'border-color 0.3s',
    },
    uploadButton: {
        borderRadius: '25px',
        padding: '10px',
        transition: 'background-color 0.3s',
    },
};

export default FilePicker;
