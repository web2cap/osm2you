import { Outlet } from 'react-router-dom';

import TopMenu from './TopMenu';

const Layout = () => {
    return (
        <div className="App">
            <TopMenu />
            <Outlet />
        </div>
    )
}

export default Layout