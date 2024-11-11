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
                        <th scope="col">Record Id</th>
                        <th scope="col">Device Id</th>
                        <th scope="col">Patient Id</th>
                        <th scope="col">Timestamp</th>
                        <th scope="col">Parameter</th>
                        <th scope="col">Value</th>
                        <th scope="col">Unit</th>
                        <th scope="col" style={{textAlign: 'center'}}>Reported</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item) => (
                        <tr key={item.id}>
                            <td>{item.record_id}</td>
                            <td>{item.device_id}</td>
                            <td>{item.patient_id}</td>
                            <td>{item.timestamp}</td>
                            <td>{item.parameter}</td>
                            <td>{item.value}</td>
                            <td>{item.unit}</td>
                            <td style={{textAlign: 'center'}}>
                                {item.reported ? <span style={{ color: 'red'}}>🔴</span> : null}
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

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`${API_BASE_URL}/api/all-data`);
                setData(response.data);
            } catch (error) {
                console.error("Error fetching data", error);
            }
        };
        fetchData();
    }, []);
    console.log(data);
    return (
        <>
            <NavBar activePage="p2"/>
            <Table data={data} />
        </>
    );
};

export default AllData
