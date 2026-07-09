<template>
<div class='container mt-5'>
<div class='row justify-content-center'>
<div class='col-md-5'>
<div class='card shadow'>
<div class='card-body'>
<h3 class='text-center mb-4'>
Trekking Mangement Login
</h3 >
<form @submit.prevent='login' >

<div class='mb-3'>
<label> Email </label>
<input type ='email' class='form-control' v-model='email' required >
</div>

<div class='mb-3' >
<label> Password </label >
<input type='password' class='form-control' v-model='password' required >
</div>

<button class='btn btn-primary w-100' >
Login </button >
</form>
<hr>
<RouterLink to ='/register'>
New User? Register Here 
</RouterLink>
</div>
</div>
</div>
</div >
</div >
</template>
<script setup>
import { ref } from 'vue'
const email= ref('')
const password = ref('')
async function login(){
    const response = await fetch("http://127.0.0.1:5000/login", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        email: email.value,
        password: password.value
    })
})
const data = await response.json()
if (response.ok){
    localStorage.setItem('token', data.token)
    localStorage.setItem('role', data.role)
    alert(data.message)
    if (data.role =='ADMIN'){
        window.location='/admin'
    }
    else if (data.role == 'STAFF'){
        window.location='/staff'
    }
    else{
        window.location='/trekker'
    }
}
else{
    alert(data.message)
}
}
</script>

