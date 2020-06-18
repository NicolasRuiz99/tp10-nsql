import React,{useEffect,useState} from "react";
import { get_user_coins, get_user_weapons, alertError, alertSuccess, alertConfirm,transfer_coins } from "../functions";
import WeaponList from "./WeaponList";

const UserAssets = ({user}) => {

    const [coins,setCoins] = useState ("");
    const [weapons,setWeapons] = useState ([]);
    const [loading,setLoading] = useState (false);
    const [target,setTarget] = useState ("");
    const [transferCoins,setTransferCoins] = useState ("");

    useEffect (()=>{
        if (user !== "Darth Vader"){
            setLoading (true);
            get_user_coins (user)
            .then (res=>{
                setCoins (res.coins);
                get_user_weapons (user)
                .then (res=>{
                    setWeapons (res);
                    setLoading (false);
                })
                .catch (err=>{
                    setLoading (false);
                    alertError ();
                })
            })
            .catch (err=>{
                setLoading (false);
                alertError ();
            })
        }        
    },[user])

    const transfer = () => {
        alertConfirm ()
        .then (res=>{
            if (res.value){
                if (target === ""){
                    alertError ();
                    return;
                }
                transfer_coins (user,target,transferCoins)
                .then (res=>{
                    alertSuccess ();
                })
                .catch (err=>{
                    alertError ();
                })
            }
        })
    }

    if (user === "Darth Vader"){
        return (
            <div>
            <h1>Transferir Galactic Coins</h1>
            <div class="form-group">
                <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">$</span>
                </div>
                <input type="number" min="1" class="form-control" onChange={e=>setTransferCoins(e.target.value)}/>
                <div class="input-group-append">
                    <select className="custom-select" onChange={e=>setTarget(e.target.value)} >
                        <option value="">Seleccionar usuario</option>
                        <option value="Boba Fett">Boba Fett</option>
                        <option value="Greedo">Greedo</option>
                        <option value="Din Djarin">Din Djarin</option>
                    </select>
                </div>
                <div class="input-group-append">
                    <button type="button" class="btn btn-success" onClick={()=> transfer()}>Transferir</button>
                </div>
                </div>
            </div>
            </div>
        );
    }else{
        return (
            <div>
                {(loading)?
                <h2>Cargando...</h2>
                :
                <div>
                    <h1>Mis Galactic Coins: {coins}</h1>
                    <h1>Mis armas</h1>
                    <WeaponList list={weapons} shop={false} user = {user}/>
                </div>
                }
            </div>
        );
    }
};

export default UserAssets;