import { Route, Routes } from "react-router-dom";

import Layout from "./Template/Layout";
import Home from "./Home/Home";
import Registration from "./User/Registration";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={
          <Home />
        } />

        <Route path="registration" element={<Registration />} />
      </Route>
    </Routes>
  );
}

export default App;
