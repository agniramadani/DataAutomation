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
                        <th scope="col">Device Type</th>
                        <th scope="col">Model</th>
                        <th scope="col">Status</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((device) => (
                        <tr key={device.id}>
                            <td>{device.device_type}</td>
                            <td>{device.model}</td>
                            <td>{device.status}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

const Devices = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const token = localStorage.getItem('appToken');
                const response = await axios.get(`${API_BASE_URL}/api/devices`, {
                    headers: {
                        // Decode token from Base64
                        Authorization: `${atob(token)}`, 
                    },
                });
                setData(response.data);
            } catch (error) {
                console.error("Error fetching device data", error);
                 // Remove token if error occurs (possibly expired or invalid)
                 localStorage.removeItem('appToken');
            }
        };
        fetchData();
    }, []);

    return (
        <>
            <NavBar activePage="p3"/>
            <Table data={data} />
        </>
    );
};

export default Devices
