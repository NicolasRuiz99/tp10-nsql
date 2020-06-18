import axios from 'axios';
import Swal from 'sweetalert2';

//alert functions

const alertSuccess = () => {
    return Swal.fire(
        'Éxito!',
        'La operación a finalizado correctamente!',
        'success'
    )
}

const alertError = () => {
    return Swal.fire({
        icon: 'error',
        title: 'Error!',
        text: 'Ocurrió un fallo!'
    })
}

const alertConfirm = () => {
    return Swal.fire({
        title: 'Confirmar operación',
        text: "Los cambios serán irreversibles!",
        icon: 'warning',
        showCancelButton: true,
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Confirmar'
    })
}

//backend request functions

const list_weapons = () => {
    return axios
        .post("http://localhost:5000/get_user_weapons", { name: "Darth Vader" })
        .then(res => {
            return res.data
        })
        .catch(err => { throw err.response.data })
}

const get_user_coins = (name) => {
    return axios
        .post("http://localhost:5000/get_user_coins", {
            name
        })
        .then(res => {
            return res.data
        })
        .catch(err => { throw err.response.data })
}

const get_user_weapons = (name) => {
    return axios
        .post("http://localhost:5000/get_user_weapons", {
            name
        })
        .then(res => {
            return res.data
        })
        .catch(err => { throw err.response.data })
}

const transfer_coins = (name1, name2, coins) => {
    return axios
        .post("http://localhost:5000/transfer_coins", {
            name1,
            name2,
            coins
        })
        .then(res => {
            return res.data
        })
        .catch(err => { throw err.response.data })
}

const buy_weapon = (weapon, user, coins) => {
    return axios
        .post("http://localhost:5000/buy_weapon", {
            weapon,
            user,
            coins
        })
        .then(res => {
            return res.data
        })
        .catch(err => { throw err.response.data })
}

export {
    alertConfirm,
    alertError,
    alertSuccess,
    list_weapons,
    get_user_coins,
    buy_weapon,
    get_user_weapons,
    transfer_coins
};