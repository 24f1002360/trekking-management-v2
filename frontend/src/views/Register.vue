<template>
<div class='container mt-5'>
<div class='row justify-content-center'>
<div class='col-md-6'>
<div class='card shadow' >
<div class='card-body'>
<h3 class='text-center md-4'>
</h3>
<form @submit.prevent='register'>
<div class='mb-3'>
<label > Name </label>
<input type='text' class='form-control' v-model='name' required>
</div >

<div class='mb-3'>
<label> Email </label>
<input type='email' class='form-control' v-model='email' required >
</div >

<div class='mb-3'>
<label> Phone</label >
<input type='text' class='form-control' v-model='phone' required>
</div>

<div class='mb-3'>
<label>Password </label >
<input type='password' class='form-control' v-model='password' required >
</div>
<button class='btn btn-success w-100'>
Register </button>
</form>
<hr>
<RouterLink to='/'>
Already have an account? 
login 
</RouterLink >
</div>
</div >
</div >
</div>
</div>

</template>
<script setup >
import {ref } from 'vue'
const name=ref('')
const email=ref('')
const phone = ref('')
const password =ref('')
async function register(){
    const response = await fetch('http://127.0.0.1:5000/register',
    {method:'POST',
    headers:{
        'Content-Type': 'application/json'
    },
    body:JSON.stringify({
        name:name.value,
        email:email.value,
        phone:phone.value,
        password:password.value,
    })
    }
    )
    const data =await response.json()
    if(response.ok){
        alert(data.message)
        window.location='/'
    }
    else{
        alert(data.message)
    }
}



</script>