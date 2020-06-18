import React,{useState,useEffect} from "react";
import { alertConfirm, alertSuccess, alertError,list_weapons,get_user_coins,buy_weapon } from "../functions";
import WeaponList from "./WeaponList";
import {withRouter} from "react-router-dom";

const Home = ({user,history}) => {

    const [weapons,setWeapons] = useState ([]);
    const [loading,setLoading] = useState (false);

    useEffect (()=>{
        setLoading (true);
        list_weapons()
        .then (res=>{
            setWeapons (res);
            setLoading (false);
        })
        .catch (err=>{
            setLoading (false);
            alertError ();
        })
    },[])

    const buyWeapon = (weapon,cost) => {
        alertConfirm ()
        .then (res=>{
            if (res.value){
                get_user_coins (user)
                .then (res=>{           
                    if (res.coins >= cost){
                        buy_weapon (weapon,user,cost)
                        .then (res=>{
                            alertSuccess ()
                            .then (()=>{
                                history.push ('/assets')
                            })
                        })
                        .catch (err=>{
                            alertError();
                            return;
                        })
                    }else{
                        throw Error ("cost")
                    }
                })
                .catch (err=>{
                    alertError ();
                    return;
                })
            }else{
                return;
            }
        })
        
    }

    return (
        <div>
            {(loading)?
            <h2>Cargando...</h2>
            :
            <WeaponList list={weapons} shop={true} user = {user} buyWeapon = {buyWeapon} />
            }       
        </div>
    );
};

export default withRouter (Home);