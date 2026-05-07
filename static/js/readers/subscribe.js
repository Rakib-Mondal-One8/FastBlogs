import { addReader } from "../api/api.js";

const subscribe = document.getElementById('subscribe');
subscribe.addEventListener('click',async (e)=>{
    const input = document.getElementById('emailId');
    const email = input.value;
    // if(!email.trim()){
    //     alert("Enter a valid email address");
    //     return;
    // }
    const data = {
        email
    }
    const response = await addReader(data)
    if(response.ok)input.value='';
    alert("Sucessfully Registered as a reader, Enjoy Reading")
    window.location.href = '/blogs'
});