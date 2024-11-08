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
                        <th scope="col">DeviceId</th>
                        <th scope="col">PatientId</th>
                        <th scope="col">MissingValues</th>
                        <th scope="col">Remarks</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item) => (
                        <tr key={item.id}>
                            <td>{item.device_id}</td>
                            <td>{item.patient_id}</td>
                            <td>{item.missing_values}</td>
                            <td>{item.remarks}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

const DataReports = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`${API_BASE_URL}/api/data-quality-checks`);
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
            <NavBar />
            <Table data={data} />
        </>
    );
};

export default DataReports;
