<template>
<div class="container mt-5" >
<h2> Staff Dashboard </h2 >
<button class='btn btn-primary mb-3' @click='loadDashboard()'> Refresh </button>

<table class='table table-bordered'>
<thead>
<tr>
<th> ID</th >
<th> Trek</th >
<th> Status</th>
<th> Available Slots</th>
<th> Participants </th >
<th> Actions</th>
</tr>
</thead>

<tbody>
<tr v-for="trek in dashboard" :key="trek.trek_id">
<td> {{ trek.trek_id }}</td>
<td> {{ trek.trek_name }}</td>
<td>
<select class='form-control' v-model='trek.status'>
<option>OPEN</option>
<option>ONGOING</option>
<option>COMPLETED</option>
</select>
</td>
<td>
<input type ='number' class='form-control' v-model='trek.available_slots'>
</td>
<td> {{ trek.registered_users }} </td>
<td>
<button class='btn btn-success btn-sm me-2' @click='updateTrek(trek)'>
Save 
</button>
<RouterLink class="btn btn-info btn-sm" :to="'/staff/participants/' + trek.trek_id">
View Participants</RouterLink>
</td>
</tr>
</tbody>
</table>

<button class='btn btn-danger' @click='logout'>
Logout </button>

</div>
</template>


<script setup>
import {ref,onMounted} from 'vue'
const dashboard=ref([])
async function loadDashboard(){
    const response=await fetch('http://127.0.0.1:5000/staff/dashboard',
    {
        headers:{
            Authorization:
            'Bearer '+localStorage.getItem('token')
        }
    })
    dashboard.value=await response.json()
}
async function updateTrek(trek){
    const response=await fetch(
        'http://127.0.0.1:5000/staff/treks/'+trek.trek_id,
        {
            method:'PUT',
            headers:{
                'Content-Type':'application/json',
                Authorization:
                'Bearer '+localStorage.getItem('token')
                },
                body:JSON.stringify({
                    available_slots:trek.available_slots,
                    status:trek.status
                    })
                    }
        )
    const data=await response.json()
    if(response.ok){
        alert(data.message)
        loadDashboard()
        }
    else{
        alert(data.message)
    }
}
function logout(){
    localStorage.clear()
    window.location='/'
}
onMounted(loadDashboard)
</script >