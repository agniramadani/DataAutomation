import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DataReports from "./components/DataReports";
import Devices from './components/Devices';
import Patients from './components/Patients';
import AllData from './components/AllData';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<DataReports />} />
        <Route path="/all-data" element={<AllData />} />
        <Route path="/devices" element={<Devices />} />
        <Route path="/patients" element={<Patients />} />
      </Routes>
    </Router>
  );
}

export default App
