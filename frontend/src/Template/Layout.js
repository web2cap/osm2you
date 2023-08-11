import { Outlet } from 'react-router-dom';

import TopMenu from './TopMenu';
import Footer from './Footer';

const Layout = () => {
    return (
        <div className="App">
            <TopMenu />
            <div className="content">
                <Outlet />
            </div>
            <Footer />
        </div>
    )
}

export default Layout