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
                        <th scope="col">Missing Values</th>
                        <th scope="col">Remarks</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item) => (
                        <tr key={item.id}>
                            <td>{item.record_id}</td>
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
            <NavBar activePage="p1"/>
            <Table data={data} />
        </>
    );
};

export default DataReports
