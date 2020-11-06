import React from 'react';
import './App.css';
import { Route, Link } from 'react-router-dom'
import Home from "./pages/Home"
import About from "./pages/About"
import Search from "./pages/Search"
import { Button } from 'react-bootstrap'
import arrow from "../src/images/arrow2.png"
import LoadingOverlay from 'react-loading-overlay'

function App() {
  const [searchloading, setSearchloading] = React.useState(false)

  return (
    <div style={{height: "100%", display: "flex", flexDirection: "column"}}>
      <LoadingOverlay active={searchloading} spinner text="Loading..." styles={{wrapper: {height: '100%'}}}>
        <body style={{minHeight: "84%"}}>
          <div style= {{margin: "2% 2% 5% 2%", display: "flex", justifyContent: "flex-end"}}>
            <Link to="/">
              <Button variant="outline-primary">홈</Button>
            </Link>
          
            <Link to="/about">
              <Button variant="outline-primary">소개</Button>
            </Link>
          </div>
          <Route path="/" exact={true} render={()=><Home setSearchloading={setSearchloading} />}/>
          <Route path="/about" component={About} exact={true}/>
        </body>
        <footer
          style={{
            width: "100%",
            height: "180px",
            backgroundColor: "#eceff1",
            color: "#757575",
            paddingLeft: "10%",
            paddingRight: "10%",
            paddingTop: "2%",
            paddingBottom: "2%"
          }}
        >
          <hr style={{ marginBottom: "10px" }} />
            <div>
              copyright® Cat Ltd. All rights Reserved.
              <br />
              대표 : CAT
              <br />
              대표연락처 : vxda7@naver.com
              <br />
            </div>
        </footer>
        <div style={{position: "fixed", bottom: "100px", right: "30px"}}>
          <a href="#"><img src={arrow} style={{height: "30px"}}/></a>
        </div>
      </LoadingOverlay>
    </div>
  );
}

export default App;
