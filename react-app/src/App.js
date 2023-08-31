import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Route, Switch } from "react-router-dom";
import SignupFormPage from "./components/SignupFormPage";
import LoginFormPage from "./components/LoginFormPage";
import { authenticate } from "./store/session";
import Navigation from "./components/Navigation";
import RunDropdown from "./components/runsDropdown";
import RunsGrid from "./components/runGrid";


function App() {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.session?.user);
  const [isLoaded, setIsLoaded] = useState(false);
  useEffect(() => {
    dispatch(authenticate()).then(() => setIsLoaded(true));
  }, [dispatch]);

  return (
    <>
      <Navigation isLoaded={isLoaded} />
      {isLoaded && (
        <Switch>
          <Route path="/login" >
            <LoginFormPage />
          </Route>
          <Route path="/signup">
            <SignupFormPage />
          </Route>
          <Route path='/'>
            {user && <RunDropdown />}
            {user && <RunsGrid />}
          </Route>
        </Switch>
      )}
    </>
  );
}

export default App;
