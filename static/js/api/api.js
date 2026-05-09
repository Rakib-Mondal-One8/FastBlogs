const BASE_URL = '/api/v1'

export async function addReader(data){

    try {
        const response = await fetch(`${BASE_URL}/readers`,{
        method:'POST',
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify(data)
        });

        if(response.ok){
            return response
        }
        else{
            const errorData = await response.json();

            if(Array.isArray(errorData.detail)){
                alert(`Error: ${errorData.detail[0].msg}`);
            }
            else{
                alert(`Error: ${errorData.detail}`);
            }
        }
    } catch (error) {
        console.error("ERROR:",error);
        alert("An error occured please try again.");
    }
}


export async function userRegistration(data){
    const payload = {
        'username':data.username,
        'email':data.email,
        'password':data.password,
        'first_name':data.first_name,
        'last_name':data.last_name,
        'phone_number':'%#$**&&@@!@@#(#',
        'role':'author'
    }

    try {
        const response = await fetch(`${BASE_URL}/auth/register`,{
        method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body: JSON.stringify(payload)
        })

        window.history.replaceState({}, document.title, window.location.pathname)

        if(response.ok){
            window.location.href = '/auth/login';
        }
        else{
            const errorData = await response.json()
            if(Array.isArray(errorData.detail) && errorData.detail[0].loc[1] == 'password'){
                alert(`Error: Password is too short`)
            }else{
                alert(`Error: ${errorData.detail}`)
            }
            
        }
    } catch (error) {
        window.history.replaceState({}, document.title, window.location.pathname)

        console.error('Error:',error)
        alert("An error occured please try again.")
    }

}


export async function userLogin(formData) {
    const payload = new URLSearchParams();
        for (const [key, value] of formData.entries()) {
            payload.append(key, value);
        }

    try {
        const response = await fetch(`${BASE_URL}/auth/token`,{
            method: 'POST',
            headers: {
                'Content-Type':'application/x-www-form-urlencoded'
            },
            body: payload
        })

        if(!response.ok){
            const error = await response.json()
            throw new error(error.detail)
        }
        
        const data = await response.json()
        console.log(data);
        window.location.href = '/'
    } catch (error) {
         console.error('Login Failed', error.message);
    }
}


// Helper function to get a cookie by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

function logout() {
    // Get all cookies
    const cookies = document.cookie.split(";");

    // Iterate through all cookies and delete each one
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const eqPos = cookie.indexOf("=");
        const name = eqPos > -1 ? cookie.slice(0, eqPos) : cookie;
        // Set the cookie's expiry date to a past date to delete it
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
    }

    // Redirect to the login page
    window.location.href = '/auth/login-page';
};


