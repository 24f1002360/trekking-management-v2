<template>
<div class='container mt-4'>
<h2> Manage Trekker</h2>
<button class="btn btn-primary mb-3" @click="loadUsers"> Refresh </button>
<RouterLink to="/admin" class="btn btn-secondary mb-3 ms-2"> Back </RouterLink>

<div class="row mb-3">
<div class="col-md-6">
<input class="form-control" placeholder="Search User..." v-model="search">
</div>
</div>

<table class='table table-bordered'>
<thead>
<tr>
<th>ID </th >
<th> Name </th>
<th> Email </th >
<th> Phone </th>
<th> Status </th>
<th> Actions </th>
</tr>
</thead>

<tbody>
<tr v-for='user in filteredUsers' :key='user.id'>
<td>{{ user.id }}</td>
<td> {{ user.name }}</td>
<td> {{ user.email }}</td >
<td> {{ user.phone }}</td>
<td> {{ user.status }}</td>
<td> 
<button class='btn btn-danger btn-sm' @click='chnageStatus(user)' >
{{ user.status=="ACTIVE" ? "Blacklist" : "Activate" }}
</button>
</td>
</tr>
</tbody>
</table>
</div >
</template>

<script setup>
import {ref , computed, onMounted} from 'vue'
const search = ref('')
const userList = ref([])
const filteredUsers = computed(()=>{
const keyword = search.value.toLowerCase()
return userList.value.filter(user=>
user.name.toLowerCase().includes(keyword) || user.email.toLowerCase().includes(keyword))
})
async function loadUser(){
    const response=await fetch('http://127.0.0.1:5000/admin/users',
    {headers:{Authorization:'Bearer '+localStorage.getItem('token')}})
    userList.value = await response.json()
}
onMounted(loadUser)
</script>

