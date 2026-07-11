<template>
<div class='container mt-4'>
<h2> Manage Trek</h2>
<button class='btn btn-primary mb-3' @click='loadTreks();loadStaff();'> Refresh </button>
<RouterLink to="/admin" class="btn btn-secondary mb-3 ms-2"> Back </RouterLink>

<div class='row mb-3'>
<div class='col-md-6'>
<input type='text' class='form-control' placeholder='Search Trek...' v-model='search' >
</div>
<div class='col-md-6 text-end'>
<button class='btn btn-success' @click='cancel(); showAddForm = true'> Add Trek </button>
</div>
</div>

<div class='card mb-4' v-if='showAddForm' >
<div class='card-body'>
<div class="row">
<h4> {{ editMode? 'Edit Trek' : 'Add Trek' }}</h4>
<div class='col-md-6 mb-3'>
<label> Name </label>
<input class='form-control' v-model='form.trek_name'>
</div>
<div class='col-md-6 mb-3'>
<label> Location </label>
<input class='form-control' v-model='form.location'>
</div>
<div class='col-md-6 mb-3'>
<label> Difficulty </label>
<select class='form-control' v-model='form.difficulty'>
<option> Easy </option>
<option> Moderate </option>
<option> Hard </option>
</select>
</div>
<div class='col-md-6 mb-3'>
<label> Duration</label>
<input type='number' class='form-control' v-model='form.duration' >
</div>
<div class='col-md-6 mb-3'>
<label> Total Slots </label>
<input type='number' class='form-control' v-model='form.total_slots'>
</div>
<div class='col-md-6 mb-3'>
<label> Status</label>
<select class='form-control' v-model='form.status'>
<option> PENDING</option>
<option> OPEN </option>
<option> CLOSED</option>
<option> ONGOING</option>
<option> COMPLETED </option>
</select>
</div>
<div class="col-md-6 mb-3">
<label>Assign Staff</label>
<select class="form-control" v-model="form.assigned_staff_id">
<option :value="null">Select Staff</option>
<option v-for="staff in staffList" :key="staff.id" :value="staff.id">
{{ staff.name }}</option>
</select>
</div>
<div class='col-md-6 mb-3'>
<label> Start Date</label>
<input type ='date' class='form-control' v-model='form.start_date'>
</div >
<div class='col-md-6 mb-3'>
<label> End Date </label>
<input type='date' class='form-control' v-model='form.end_date'>
</div>
<div class='col-12 mb-3'>
<label> Description</label>
<textarea class='form-control' v-model='form.description'> </textarea>
</div>
</div>

<button class='btn btn-primary' @click='saveTrek' >
{{ editMode ? 'Update Trek' : 'Create Trek' }} </button>
<button class='btn btn-secondary ms-2' @click='cancel'>  Cancel </button>
</div>
</div >



<table class='table table-bordered'>
<thead>
<tr>
<th>ID </th >
<th> Name </th>
<th> Location </th >
<th> Status </th>
<th> Staff ID </th>
<th> Actions </th>
</tr>
</thead>

<tbody>
<tr v-for='trek in filteredTreks' :key='trek.id'>
<td>{{ trek.id }}</td>
<td> {{ trek.trek_name }}</td>
<td> {{ trek.location }}</td >
<td> {{ trek.status }}</td>
<td> {{ trek.assigned_staff_name }}</td>
<td> 
<button class='btn btn-warning btn-sm me-2' @click='editTrek(trek)' > Edit
</button>
<button class='btn btn-danger btn-sm me-2' @click='deleteTrek(trek.id)' > Delete </button>
</td> 
</tr>
</tbody>
</table>
</div>
</template>

<script setup>
import {ref , computed, onMounted} from 'vue'
const trekList = ref([])
const staffList = ref([])
const search = ref('')
const editMode = ref(false)
const showAddForm = ref(false)
const form = ref({
    trek_name:'',
    location:'',
    difficulty:'Easy',
    duration:1,
    total_slots:10,
    available_slots:10,
    status:'PENDING',
    assigned_staff_id:null,
    description:'',
    start_date:'',
    end_date:''
})
async function loadStaff(){
    const response = await fetch(
        'http://127.0.0.1:5000/admin/staff',
        {headers:{
                Authorization:
                'Bearer '+localStorage.getItem('token')
            }
        }
    )
    const data = await response.json()
    console.log(data)
    staffList.value = data
}
async function loadTreks(){
    const response=await fetch('http://127.0.0.1:5000/treks',
    {headers:{Authorization:'Bearer '+localStorage.getItem('token')}})
    const data = await response.json()
    console.log(data)
    trekList.value=data
}
const filteredTreks = computed(()=>{
    const keyword = search.value.toLowerCase()
    return trekList.value.filter(
        trek => 
            trek.trek_name.toLowerCase().includes(keyword) ||
            trek.location.toLowerCase().includes(keyword)
    )
})
async function saveTrek() {

    let url = 'http://127.0.0.1:5000/treks'
    let method = 'POST'

    if (editMode.value) {
        url += '/' + form.value.id
        method = 'PUT'
    }

    const response = await fetch(url, {
        method,
        headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify(form.value)
    })

    const data = await response.json()

    if (!response.ok) {
        alert(data.message)
        return
    }

    alert(data.message)

    cancel()

    loadTreks()
}

function editTrek(trek){
    form.value={...trek}
    editMode.value=true
    showAddForm.value=true
}
async function deleteTrek(id){
    if(!confirm('Delete Trek')) return
    await fetch('http://127.0.0.1:5000/treks/'+id,
    {method:'DELETE',
    headers:{
        Authorization:
        'Bearer '+localStorage.getItem('token')
    }})
    alert('Trek Deleted Successfully')
    loadTreks()
}
function cancel(){
    editMode.value=false
    showAddForm.value=false
    form.value = {
    
        trek_name:'',

        location:'',

        difficulty:'Easy',

        duration:1,

        total_slots:10,

        available_slots:10,

        status:'PENDING',

        assigned_staff_id:null,

        description:'',

        start_date:'',

        end_date:''

    }
}
onMounted(()=>{
    loadTreks()
    loadStaff()
})
</script>

