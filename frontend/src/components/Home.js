import React,{useState,useEffect} from "react";
import { alertConfirm, alertSuccess, alertError,list_weapons,get_user_coins,buy_weapon } from "../functions";
import WeaponList from "./WeaponList";
import {withRouter} from "react-router-dom";

const Home = ({user,history}) => {

    const [weapons,setWeapons] = useState ([{name:'Sable de luz',cost:6},{name:'Blaster',cost:4}]);
    const [loading,setLoading] = useState (false);

    /*
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
    */

    const buyWeapon = (weapon,cost) => {
        alertConfirm ()
        .then (res=>{
            if (res.value){
                let user_coins;
                get_user_coins (user)
                .then (res=>{
                    user_coins = res.coins;
                })
                .catch (err=>{
                    alertError ();
                    return;
                })
                if (user_coins >= cost){
                    buy_weapon (weapon,user,user_coins-cost)
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
                }
            }else{
                return;
            }
        })
        
    }

    return (
        <WeaponList list={weapons} shop={true} user = {user} buyWeapon = {buyWeapon} />
    );
};

export default withRouter (Home);