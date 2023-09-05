import React from 'react';
import { NavLink } from 'react-router-dom';
import { useSelector } from 'react-redux';
import ProfileButton from './ProfileButton';
import './Navigation.css';

function Navigation({ isLoaded }){
	const sessionUser = useSelector(state => state.session.user);

	return (
	  <nav className="navbar">
		<ul className="nav-list">
		  <li className="nav-item">
			<NavLink exact to="/" className="nav-link">Home</NavLink>
		  </li>
		  {isLoaded && (
			<li className="nav-item">
			  <ProfileButton user={sessionUser} />
			</li>
		  )}
		</ul>
	  </nav>
	);
}

export default Navigation;
