<template>
<div class='container mt-4'>
<h2>My Profile</h2>

<RouterLink to='/trekker' class='btn btn-secondary mb-3'> Back </RouterLink>

<div class='card' >
<div class='card-body'>

<div class='mb-3' >
<label> Name </label>
<input class='form-control' v-model='form.name'> 
</div>

<div class='mb-3' >
<label> Email </label>
<input class= 'form-control' v-model='form.email' disabled>
</div>

<div class='mb-3'>
<label> Phone </label>
<input class='form-control' v-model='form.phone'>
</div>

<button class ='btn btn-primary' @click='saveProfile' > Update Profile </button>

</div >
</div >
</div >
</template >

<script setup>
import { ref,onMounted } from 'vue'
const form =ref({
    name:"",
    email:"",
    phone:""
})
async function loadProfile(){
    const response =await fetch(
        'http://127.0.0.1:5000/trekker/profile',
        {
            headers:{
                Authorization:
                "Bearer "+localStorage.getItem("token")
            }
        }
    )
    const data =await response.json()
    if(!response.ok){
        alert(data.message)
        return
    }
    form.value = data
}

async function saveProfile(){
    const response =await fetch(
        'http://127.0.0.1:5000/trekker/profile',
        {
            method:"PUT",
            headers:{
                "Content-Type":"application/json",
                Authorization:
                "Bearer "+localStorage.getItem("token")
            },
            body:JSON.stringify(form.value)
        }
    )
    const data = await response.json()
    alert(data.message)
    if(response.ok){
        loadProfile()
    }
}

onMounted(loadProfile)

</script>