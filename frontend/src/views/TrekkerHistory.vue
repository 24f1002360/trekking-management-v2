<template>
<div class='container mt-4' >
<h2> Trekking History </h2>

<button class='btn btn-primary mb-3' @click="loadHistory"> Refresh </button>
<RouterLink to='/trekker' class='btn btn-secondary mb-3 ms-2'> Back </RouterLink>

<table class='table table-bordered'>
<thead>
<tr>
<th>Name </th >
<th>Location</th >
<th> Difficulty </th >
<th>Completed On </th>
</tr>
</thead>

<tbody>
<tr v-for='trek in history'
:key="trek.trek_name">

<td>{{ trek.trek_name }} </td > 
<td>{{ trek.location }} </td >
<td>{{ trek.difficulty }} </td>
<td> {{ trek.completed_on }}</td >
</tr >
</tbody>
</table>

</div>
</template >

<script setup>
import { ref,onMounted } from 'vue'
const history = ref([])
async function loadHistory(){
    const response =await fetch(
        "http://127.0.0.1:5000/trekker/history",
        {
            headers:{
                Authorization:
                "Bearer "+localStorage.getItem('token')
                }
            }
    )
    const data=await response.json()
    if(!response.ok){
        alert(data.message)
        return
        }
    history.value=data
}

onMounted(loadHistory)

</script>