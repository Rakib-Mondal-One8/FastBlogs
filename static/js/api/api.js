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




