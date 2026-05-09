import { userRegistration } from "../api/api.js"

const registerForm = document.getElementById('registerForm')
if(registerForm){
    registerForm.addEventListener('submit',async(e)=>{
        e.preventDefault()

        const form = e.target
        const formData = new FormData(form)
        const data = Object.fromEntries(formData.entries())

        
        if(data.password!==data.password2){
            alert("Passwords do not match");
            return;
        }

        await userRegistration(data)
    })
}