import React,{Fragment,useState} from 'react';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import './bootstrap.min.css'
import Navbar from './components/Navbar';
import Home from './components/Home';
import UserAssets from './components/UserAssets';

const App = () => {

	const [user,setUser] = useState ("");

	return (
		<Fragment>
			<Router>
			<Navbar user={user} setUser={setUser} />
			<Switch>
				<Route exact path="/" render={()=>(
					<Home user={user} />
				)} />
				<Route exact path="/assets" render={()=>(
					<UserAssets user={user} />
				)} />
			</Switch>
			</Router>
		</Fragment>
	);
}

export default App;