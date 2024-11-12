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
                        <th scope="col">Name</th>
                        <th scope="col">Date of Birth</th>
                        <th scope="col">Contact Info</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((patient) => (
                        <tr key={patient.id}>
                            <td>{patient.name}</td>
                            <td>{new Date(patient.date_of_birth).toLocaleDateString()}</td>
                            <td>{patient.contact_info}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

const Patients = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const token = localStorage.getItem('appToken');
                const response = await axios.get(`${API_BASE_URL}/api/patients`, {
                    headers: {
                        // Decode token from Base64
                        Authorization: `${atob(token)}`, 
                    },
                });
                setData(response.data);
            } catch (error) {
                console.error("Error fetching patient data", error);
                 // Remove token if error occurs (possibly expired or invalid)
                 localStorage.removeItem('appToken');
            }
        };
        fetchData();
    }, []);
    
    return (
        <>
            <NavBar activePage="p4"/>
            <Table data={data} />
        </>
    );
};

export default Patients
