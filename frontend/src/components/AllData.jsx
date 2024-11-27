import { useEffect, useState } from 'react';
import axios from 'axios';
import NavBar from "./Navbar";
import { API_BASE_URL } from './APIconfig';

const FeedbackModal = ({ show, feedbackText, onFeedbackChange, handleSubmition, handleClose }) => {
    // Render nothing if show is false
    if (!show) return null;

    return (
        <div className="modal fade show d-block" tabIndex="-1" role="dialog" style={{ backgroundColor: 'rgba(0, 0, 0, 0.5)' }}>
            <div className="modal-dialog" role="document">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title">Modal Title</h5>
                    </div>
                    <div className="modal-body">
                        <input 
                            type="text" 
                            className="form-control" 
                            placeholder="Enter your feedback"
                            value={feedbackText}
                            onChange={(e) => onFeedbackChange(e.target.value)}
                        />
                    </div>
                    <div className="modal-footer">
                        <button type="button" className="btn btn-primary" onClick={handleSubmition}>
                            Submit
                        </button>
                        <button type="button" className="btn btn-secondary" onClick={handleClose}>
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

const Table = ({ data, onFeedbackClick }) => {
    return (
        <div style={{ margin: '40px' }}>
            <table className="table table-bordered">
                <thead>
                    <tr>
                        <th scope="col">Record Id</th>
                        <th scope="col">Device Id</th>
                        <th scope="col">Patient Id</th>
                        <th scope="col">Timestamp</th>
                        <th scope="col">Parameter</th>
                        <th scope="col">Value</th>
                        <th scope="col">Unit</th>
                        <th scope="col" style={{ textAlign: 'center' }}>Reported</th>
                        <th scope="col" style={{ textAlign: 'center' }}>Feedback</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item, index) => (
                        <tr key={index}>
                            <td>{item.record_id}</td>
                            <td>{item.device_id}</td>
                            <td>{item.patient_id}</td>
                            <td>{item.timestamp}</td>
                            <td>{item.parameter}</td>
                            <td>{item.value}</td>
                            <td>{item.unit}</td>
                            <td style={{ textAlign: 'center' }}>
                                {item.reported ? <span style={{ color: 'red' }}>🔴</span> : null}
                            </td>
                            <td style={{ textAlign: 'center' }}>
                                <button className='btn btn-info' onClick={() => onFeedbackClick(item.record_id, item.device_id, item.patient_id)}> → </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

const AllData = () => {
    const [data, setData] = useState([]);
    const [showModal, setShowModal] = useState(false);

    // These data will be used to submit a feedback
    const [feedbackText, setFeedbackText] = useState('');
    const [recordId, setRecordId] = useState(null);
    const [deviceId, setDeviceId] = useState(null);
    const [patientId, setPatientId] = useState(null);
    const [userId, setUserId] = useState(null);

    const feedbackHandler = (recordId, deviceId, patientId) => {
        // Clear any previous feedback text to start fresh
        setFeedbackText('');
        // Display the feedback modal
        setShowModal(true);
        // Set identifiers for the selected item
        setRecordId(recordId);
        setDeviceId(deviceId);
        setPatientId(patientId);
        setUserId(atob(localStorage.getItem('userId')));
    };

    const feedbackSubmit = async () => {
        try {
            const token = localStorage.getItem('appToken');
            await axios.post(`${API_BASE_URL}/api/feedback`,
                {
                    'record_id': recordId,
                    'device_id': deviceId,
                    'patient_id': patientId,
                    'user_id': userId,
                    'feedback_text': feedbackText
                },
                {
                    headers: {
                        Authorization: `${atob(token)}`, 
                    }
                }
            );
            setShowModal(false);
            setFeedbackText(null);
            alert('Your feedback has been sent!')
        } catch (error) {
            console.error("Error submitting feedback", error);
            localStorage.removeItem('appToken');
            localStorage.removeItem('userId');
        }
    };

    // Function to handle feedback text change
    const handleFeedbackChange = (text) => {
        setFeedbackText(text);
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const token = localStorage.getItem('appToken');
                const response = await axios.get(`${API_BASE_URL}/api/all-data`, {
                    headers: {
                        Authorization: `${atob(token)}`, 
                    },
                });
                setData(response.data);
            } catch (error) {
                console.error("Error fetching data", error);
                localStorage.removeItem('appToken');
                localStorage.removeItem('userId');
            }
        };
        fetchData();
    }, []);

    return (
        <>
            <NavBar activePage="p2" />
            <Table data={data} onFeedbackClick={feedbackHandler} />
            <FeedbackModal 
                show={showModal} 
                feedbackText={feedbackText} 
                onFeedbackChange={handleFeedbackChange}
                handleClose={() => setShowModal(false)} 
                handleSubmition={feedbackSubmit}
            />
        </>
    );
};

export default AllData;
