import { userLogin } from "../api/api.js"


const loginForm = document.getElementById('loginForm')

if(loginForm){
    loginForm.addEventListener('submit',async (e)=>{
        e.preventDefault()

        const form = e.target
        const formData = new FormData(form)

        
        await userLogin(formData)
    })
}