<template>
<div class='container mt-4'>
<h2>Trekker Dashboard</h2 >

<div class='row mt-4' >

<div class='col-md-4' >
<div class='card text-center'>
<div class='card-body'>
<h5>Available Treks</h5>
<h2> {{ dashboard.available_treks }} </h2 >
</div >
</div >
</div >

<div class='col-md-4'>
<div class='card text-center'>
<div class='card-body'>
<h5>My Bookings</h5>
<h2>{{ dashboard.my_bookings }}</h2>
</div>
</div>
</div>

</div>

<hr>
<div class='mt-4'>

<RouterLink to='/trekker/treks' class='btn btn-primary me-2'>
Available Treks
</RouterLink>

<RouterLink to='/trekker/bookings' class='btn btn-success me-2' >
My Bookings
</RouterLink >

<RouterLink to='/trekker/history' class='btn btn-warning me-2'>
History
</RouterLink >

<RouterLink to='/trekker/profile' class='btn btn-info me-2' >
Profile
</RouterLink>

</div>
<hr>

<button class='btn btn-danger' @click='logout'>
Logout
</button >
</div>
</template>

<script setup>
import { ref,onMounted } from 'vue'
const dashboard =ref({})

async function loadDashboard(){
    const response = await fetch(
        'http://127.0.0.1:5000/trekker/dashboard',
        {
            headers:{
                Authorization:
                'Bearer '+localStorage.getItem("token")
                }
            }
    )
    const data = await response.json()
    if(!response.ok){
        alert(data.message)
        return
    }
dashboard.value = data
}

function logout(){
    localStorage.clear()
    window.location= '/'
}

onMounted(loadDashboard)

</script>