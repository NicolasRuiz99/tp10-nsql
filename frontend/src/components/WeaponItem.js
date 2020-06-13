import React from "react"

const WeaponItem = ({item,shop,user,buyWeapon}) => {

    if (shop) {
        return (
            <tr>
            <th>{item.name}</th>
            <th>{item.cost}</th>
            {(user !== "" && user !== "Darth Vader")?
            <th><button type="button" className="btn btn-success" onClick={()=>buyWeapon(item.name,item.cost)} >Comprar</button></th>
            :
            <th><button type="button" className="btn btn-success" disabled>Comprar</button></th>
            }
            </tr>
        );
    }else{
        return (
            <tr>
            <th>{item.name}</th>
            <th>{item.cost}</th>
            </tr>
        );
    }
};

export default WeaponItem;