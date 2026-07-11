<template>
<div class="container mt-4">
<h2>Participants</h2>

<RouterLink to="/staff" class="btn btn-secondary mb-3">
Back
</RouterLink>

<div class='row mb-3'>
<div class="col-md-6" >
<input class="form-control" placeholder="Search Participant..." v-model="search">
</div>
</div>

<table class='table table-bordered'>
<thead>
<tr>
<th>ID </th>
<th>Name </th >
<th>Email </th>
<th>Phone </th>
<th>Status </th>
</tr>
</thead>

<tbody>
<tr v-for="participant in filteredParticipants" :key='participant.booking_id'>
<td> {{ participant.booking_id }} </td >
<td>{{ participant.user_name }}</td >
<td>{{ participant.email }}</td>
<td>{{ participant.phone }}</td>
<td>{{ participant.status }}</td>
</tr >
</tbody>
</table >
</div>
</template>

<script setup>
import {ref,computed,onMounted} from 'vue'
import {useRoute} from "vue-router"
const route = useRoute()
const participants = ref([])
const search = ref('')
async function loadParticipants(){
const response = await fetch(
    'http://127.0.0.1:5000/staff/' + route.params.id + '/participants',
    {
        headers:{
            Authorization:
            'Bearer '+localStorage.getItem('token')
            }
            }
    )
participants.value = await response.json()
}

const filteredParticipants = computed(()=>{
    const keyword = search.value.toLowerCase()
    return participants.value.filter(
        p =>
        p.user_name.toLowerCase().includes(keyword) ||
        p.email.toLowerCase().includes(keyword))
})

onMounted(loadParticipants)
</script>