import React from "react"
import {Link} from "react-router-dom";

const Navbar = ({user,setUser}) => {
    return (
        <div className="navbar navbar-expand-lg navbar-light bg-light">
            <Link className="navbar-brand" to="/">BlockchainDB Galáctico</Link>
            <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarColor03" aria-controls="navbarColor03" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarColor03">
                <ul className="navbar-nav mr-auto">
                <li className="nav-item">
                    <Link className="nav-link" to="/">Tienda</Link>
                </li>
                {(user !== "")?
                    <li className="nav-item">
                    <Link className="nav-link" to="/assets">Mis Activos</Link>
                    </li>
                :
                null
                }
                
                </ul>
                <form className="form-inline my-2 my-lg-0">
                    <select className="custom-select" onChange={e=>setUser(e.target.value)} >
                        <option value="">Seleccionar usuario</option>
                        <option value="Darth Vader">Darth Vader</option>
                        <option value="Boba Fett">Boba Fett</option>
                        <option value="Greedo">Greedo</option>
                        <option value="Din Djarin">Din Djarin</option>
                    </select>
                </form>
            </div>
        </div>
    );
};

export default Navbar;