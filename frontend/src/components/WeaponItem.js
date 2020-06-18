import React from "react"

const WeaponItem = ({item,shop,user,buyWeapon}) => {

    if (shop) {
        return (
            <tr>
            <th>{item.data.name}</th>
            <th>{item.data.cost}</th>
            <th>{item.amount}</th>
            {(user !== "" && user !== "Darth Vader")?
            <th><button type="button" className="btn btn-success" onClick={()=>buyWeapon(item.id,item.data.cost)} >Comprar</button></th>
            :
            <th><button type="button" className="btn btn-success" disabled>Comprar</button></th>
            }
            </tr>
        );
    }else{
        return (
            <tr>
            <th>{item.data.name}</th>
            <th>{item.data.cost}</th>
            <th>{item.amount}</th>
            </tr>
        );
    }
};

export default WeaponItem;