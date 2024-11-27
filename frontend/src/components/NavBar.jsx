const NavBar = ({ activePage }) => {
    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
            <div className="container-fluid">
                <a className="navbar-brand" href="/">DataAutomation</a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        <li className="nav-item">
                            <a className={`nav-link ${activePage === 'p1' ? 'active' : ''}`} href="/">Data Reports</a>
                        </li>
                        <li className="nav-item">
                            <a className={`nav-link ${activePage === 'p2' ? 'active' : ''}`} href="all-data">All Data</a>
                        </li>
                        <li className="nav-item">
                            <a className={`nav-link ${activePage === 'p3' ? 'active' : ''}`} href="devices">Devices</a>
                        </li>
                        <li className="nav-item">
                            <a className={`nav-link ${activePage === 'p4' ? 'active' : ''}`} href="patients">Patients</a>
                        </li>
                        <li className="nav-item">
                            <a className={`nav-link ${activePage === 'p5' ? 'active' : ''}`} href="feedbacks">Feedbacks</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default NavBar;
