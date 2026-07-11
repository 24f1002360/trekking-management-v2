<template>
<div class="container mt-5" >

<h2 > Admin Dashboard </h2 >
<div class='row mt-4' >

<div class='col-md-3'>
<div class='card text-center'>
<div class='card-body'>
<h5> Total Treks </h5 >
<h2> {{ dashboard.total_treks }}</h2>
</div >
</div>
</div >

<div class='col-md-3'>
<div class='card text-center'>
<div class='card-body' >
<h5> Total Staff </h5>
<h2> {{ dashboard.total_staff }}</h2 >
</div >
</div >
</div>

<div class ='col-md-3'>
<div class='card text-center'>
<div class='card-body' >
<h5> Total  trekkers </h5 >
<h2> {{ dashboard.total_users }} </h2>
</div>
</div>
</div>

</div>

<hr>
<div class='mt-4'>
<RouterLink to ='/admin/treks' class='btn btn-primary me-2'> Manage Treks
</RouterLink>
<RouterLink to='/admin/staff' class='btn btn-success me-2' > Manage Staff
</RouterLink >
<RouterLink to='/admin/users' class='btn btn-warning me-2'> Manage users
</RouterLink>
<RouterLink to='/admin/bookings' class='btn btn-info me-2'> View bookings
</RouterLink>
</div>

<hr>
<button class='btn btn-danger' @click='logout'> Logout </button>

</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const dashboard = ref({})
async function loadDashboard(){
    const response= await fetch('http://127.0.0.1:5000/admin/dashboard',
    {headers:{Authorization: 'Bearer '+localStorage.getItem('token')}})
    dashboard.value=await response.json()
}
function logout(){
    localStorage.clear()
    window.location='/'
}
onMounted(loadDashboard)
</script>