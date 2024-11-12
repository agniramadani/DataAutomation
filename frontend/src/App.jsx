import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import DataReports from "./components/DataReports";
import Devices from './components/Devices';
import Patients from './components/Patients';
import AllData from './components/AllData';
import Login from './components/Login';

function App() {
  const token = localStorage.getItem('appToken');
  return (
    <Router>
      <Routes>
        {!token ? (
          <Route path="*" element={<Login />} />
        ) : (
          <>
            <Route path="/" element={<DataReports />} />
            <Route path="/all-data" element={<AllData />} />
            <Route path="/devices" element={<Devices />} />
            <Route path="/patients" element={<Patients />} />
            <Route path="/login" element={<Navigate replace to="/" />} />
          </>
        )}
      </Routes>
    </Router>
  );
}

export default App
