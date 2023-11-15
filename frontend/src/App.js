import { useEffect } from "react";
import { Route, Routes } from "react-router-dom";
import { useStoreActions, useStoreState } from 'easy-peasy'

import Layout from "./Template/Layout";
import Home from "./Home/Home";
import Registration from "./User/Registration";
import Login from "./User/Login";
import Logout from "./User/Logout";
import Missing from "./Template/Missing";
import userAuth from "./User/hooks/userAuth";

import MarkerInstance from "./Map/MarkerInstance";
import EditMarker from "./Map/EditMarker";

function App() {

  const DEBUG = useStoreState((state) => state.DEBUG)

  const user = useStoreState((state) => state.user)
  const setUser = useStoreActions((actions) => actions.setUser)

  const accessToken = useStoreState((state) => state.accessToken)
  const setAccessToken = useStoreActions((actions) => actions.setAccessToken)

  const backend = useStoreState((state) => state.backend)
  const setBackendHeader = useStoreActions((actions) => actions.setBackendHeader)
  const unsetBackendHeader = useStoreActions((actions) => actions.unsetBackendHeader)


  useEffect(() => {
    userAuth(accessToken, setAccessToken, setUser, backend, setBackendHeader, unsetBackendHeader)
  }, [accessToken])


  useEffect(() => {
    // print user
    if (DEBUG) console.log(user)
  }, [user])

  

  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={
          <Home />
        } />
        <Route path="user">
          <Route path="registration" element={<Registration />} />
          <Route path="login" element={<Login />} />
          <Route path="logout" element={<Logout />} />
        </Route>
        <Route path="markers">
          <Route path=":id" element={<MarkerInstance />} />
          <Route path="edit/:id" element={<EditMarker />} />
        </Route>
        <Route path="*" element={<Missing />} />
      </Route>
    </Routes>
  );
}

export default App;
