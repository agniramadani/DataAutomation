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
                const response = await axios.get(`${API_BASE_URL}/api/patients`);
                setData(response.data);
            } catch (error) {
                console.error("Error fetching patient data", error);
            }
        };
        fetchData();
    }, []);
    
    return (
        <>
            <NavBar />
            <Table data={data} />
        </>
    );
};

export default Patients;
