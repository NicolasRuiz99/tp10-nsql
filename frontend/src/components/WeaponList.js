import React from "react"
import WeaponItem from "./WeaponItem";

const WeaponList = ({ list, shop,user,buyWeapon }) => {
    return (
        <table className="table table-hover">
        <thead>
            <tr>
            <th scope="col">Arma</th>
            <th scope="col">Precio (Galactic Coins)</th>
            <th scope="col">Cantidad</th>
            {(shop)?
            <th scope="col">Acción</th>
            :
            null
            }
            </tr>
        </thead>
        <tbody>
            {list.map((item)=>(
                <WeaponItem key={item.id} item={item} shop={shop} user = {user} buyWeapon={buyWeapon} />
            ))}
        </tbody>
        </table>
    );
};

export default WeaponList;