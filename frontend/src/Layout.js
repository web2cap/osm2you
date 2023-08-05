import { Outlet } from 'react-router-dom';

import TopMenu from './Template/TopMenu';

const Layout = () => {
    return (
        <div className="App">
            <TopMenu />
            <Outlet />
        </div>
    )
}

export default Layout