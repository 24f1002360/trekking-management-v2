<template>
<div class='container mt-4'>
<h2> Manage Staff</h2>
<button class='btn btn-primary mb-3' @click='loadStaff'> Refresh </button>
<RouterLink to="/admin" class="btn btn-secondary mb-3 ms-2"> Back </RouterLink>

<div class='row mb-3'>
<div class='col-md-6'>
<input type='text' class='form-control' placeholder='Search Staff...' v-model='search' >
</div>
<div class='col-md-6 text-end'>
<button class='btn btn-success' @click='cancel(); showAddForm=true'>
Add Staff </button>
</div>
</div>

<div class='card mb-4' v-if='showAddForm'>
<div class='card-body'> 
<h4> 
{{ editMode ? 'Edit Staff' : 'Add Staff' }}
</h4>
<div class='row'>

<div class='col-md-6 mb-3'>
<label> Name </label>
<input class='form-control' v-model='form.name' >
</div>

<div class='col-md-6 mb-3'> 
<label> Email </label>
<input type='email' class='form-control' v-model='form.email'>
</div>

<div class='col-md-6 mb-3'>
<label> Phone </label>
<input class='form-control' v-model='form.phone'>
</div>

<div class='col-md-6 mb-3' v-if='!editMode' >
<label> Password </label>
<input type='password' class='form-control' v-model='form.password' required >
</div>

<div class='col-md-6 mb-3'>
<label> Status </label>
<select class='form-control' v-model='form.status' >
<option> ACTIVE</option >
<option> BLACKLISTED </option>
</select>
</div>
</div>

<button class='btn btn-primary' @click='saveStaff'>
{{ editMode ? 'Update Staff' : 'Create Staff'}}
</button>
<button class='btn btn-secondary ms-2' @click='cancel'>
Cancel </button >
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
<tr v-for='staff in filteredStaff' :key='staff.id'>
<td>{{ staff.id }}</td>
<td> {{ staff.name }}</td>
<td> {{ staff.email }}</td >
<td> {{ staff.phone }}</td>
<td> {{staff.status }}</td>
<td> 
<button class='btn btn-warning btn-sm me-2' @click ='editStaff(staff)'> Edit </button>
<button class='btn btn-danger btn-sm' @click='changeStatus(staff)'> 
{{ staff.status == 'ACTIVE' ? 'Blacklist' : 'Activate' }}</button>
</td>
</tr>
</tbody>
</table>
</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
const staffList = ref([])
const search = ref('')
const editMode = ref(false)
const showAddForm = ref(false)
const form = ref({
    name:'',
    email:'',
    phone:'',
    password:'',
    status:'ACTIVE'
})

async function loadStaff(){
    const response = await fetch(
        'http://127.0.0.1:5000/admin/staff',
        {
            headers:{
                Authorization:
                'Bearer '+localStorage.getItem('token')
            }
        }
    )
    staffList.value = await response.json()

}

const filteredStaff = computed(()=>{
    const keyword = search.value.toLowerCase()
    return staffList.value.filter(
        staff =>
        staff.name.toLowerCase().includes(keyword) ||
        staff.email.toLowerCase().includes(keyword) ||
        (staff.phone || "").toLowerCase().includes(keyword)
        )
})

async function saveStaff(){
    let url='http://127.0.0.1:5000/admin/staff'
    let method='POST'
    if(editMode.value){
        url += '/'+form.value.id
        method='PUT'
    }
    const response = await fetch(
    url,
    {
        method,
        headers:{
            "Content-Type":"application/json",
            Authorization:
            "Bearer "+localStorage.getItem("token")
        },
        body:JSON.stringify(form.value)
        }
    )
    const data = await response.json()
    if(!response.ok){
        alert(data.message)
    return}
    console.log(data)
    alert(data.message)
    cancel()
    loadStaff()

}

function editStaff(staff){
    form.value = {...staff}
    editMode.value = true
    showAddForm.value = true
}

async function changeStatus(staff){
    let status='ACTIVE'
    if(staff.status=='ACTIVE'){
        status='BLACKLISTED'
    }
    await fetch(
        'http://127.0.0.1:5000/admin/staff/'+staff.id+'/status',
        {
            method:'PUT',
            headers:{
                'Content-Type':'application/json',
                Authorization:
                'Bearer '+localStorage.getItem('token')
            },
            body:JSON.stringify({
                status:status
            })
        }
    )
    alert('Status Updated')
    loadStaff()

}

function cancel(){
    editMode.value=false
    showAddForm.value=false
    form.value={
        name:'',
        email:'',
        phone:'',
        password:'',
        status:'ACTIVE'
    }
}
onMounted(loadStaff)

</script>