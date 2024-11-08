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
                const response = await axios.get(`${API_BASE_URL}/api/devices`);
                setData(response.data);
            } catch (error) {
                console.error("Error fetching device data", error);
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

export default Devices;
