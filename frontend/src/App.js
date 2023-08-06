import { useEffect, useState } from "react";
import { Route, Routes } from "react-router-dom";


import Layout from "./Template/Layout";
import Home from "./Home/Home";
import Registration from "./User/Registration";
import Login from "./User/Login";
import userGetMe from "./User/hooks/userGetMe";

function App() {
  const [user, setUser] = useState('')
  const [accessToken, setAccessToken] = useState(
    localStorage.getItem('accessToken')
  )

  useEffect(() => { userGetMe(accessToken, setAccessToken, setUser) }, [accessToken])

  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={
          <Home />
        } />
        <Route path="user">
          <Route path="registration" element={<Registration />} />
          <Route path="login" element={<Login />} />
        </Route>
      </Route>
    </Routes>
  );
}

export default App;
