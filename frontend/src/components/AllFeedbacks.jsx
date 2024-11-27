import { useEffect, useState } from 'react';
import axios from 'axios';
import NavBar from "./Navbar";
import { API_BASE_URL } from './APIconfig';

const Table = ({ data }) => {
    return (
        <div style={{ margin: '40px' }}>
            <table className="table table-bordered">
                <thead>
                    <tr>
                        <th scope="col">Device Id</th>
                        <th scope="col">Patient Id</th>
                        <th scope="col">User Id</th>
                        <th scope="col">Timestamp</th>
                        <th scope="col">Feedback</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item) => (
                        <tr key={item.feedback_id}>
                            <td>{item.device_id}</td>
                            <td>{item.patient_id}</td>
                            <td>{item.user_id}</td>
                            <td>{item.timestamp}</td>
                            <td style={{maxWidth:'200px', overflowX: 'auto', whiteSpace: 'nowrap'}}>
                                {item.feedback_text}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

const AllFeedbacks = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const token = localStorage.getItem('appToken');
                const response = await axios.get(`${API_BASE_URL}/api/all-feedbacks`, {
                    headers: {
                        // Decode token from Base64
                        Authorization: `${atob(token)}`, 
                    },
                });
                setData(response.data);
            } catch (error) {
                console.error("Error fetching patient data", error);
                // Remove token and userId if error occurs (possibly expired or invalid)
                localStorage.removeItem('appToken');
                localStorage.removeItem('userId');
            }
        };
        fetchData();
    }, []);
    
    return (
        <>
            <NavBar activePage="p5"/>
            <Table data={data} />
        </>
    );
}

export default AllFeedbacks;
