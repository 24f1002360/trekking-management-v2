<template>
<div class='container mt-4'>

<h2>Available Treks</h2>

<div class='mb-3' >
<button class='btn btn-primary' @click='loadTreks'> Refresh </button >
<RouterLink to='/trekker' class='btn btn-secondary ms-2'> Back </RouterLink>
</div>

<div class='row mb-3' >

<div class="col-md-6" >
<input class='form-control' placeholder="Search Trek..." v-model='search' >
</div>

<div class="col-md-3">
<input type='number' class= 'form-control' placeholder="Duration (Days)" v-model="durationFilter">
</div>

<div class='col-md-3'>
<select class="form-control" v-model='difficultyFilter' >
<option value=""> All Difficulties </option >
<option>Easy </option >
<option>Moderate </option >
<option>Hard </option >
</select>
</div>

</div>

<table class='table table-bordered' >
<thead >
<tr>
<th>ID </th>
<th> Name </th>
<th> Location </th>
<th> Difficulty </th >
<th> Duration </th >
<th> Available Slots </th >
<th> Actions</th >
</tr>
</thead>

<tbody>
<tr 
v-for="trek in filteredTreks"
:key="trek.id">

<td>{{ trek.id }} </td>
<td>{{ trek.trek_name }}</td >
<td>{{ trek.location }} </td>
<td>{{ trek.difficulty }} </td>
<td>{{ trek.duration }} Days </td>
<td>{{ trek.available_slots }} </td>
<td >
<button class="btn btn-success btn-sm me-2" @click='bookTrek(trek.id)'> Book </button>

<button class='btn btn-info btn-sm' @click='viewDetails(trek.id)'>View </button>
</td>
</tr>
</tbody>
</table>

<div
v-if="selectedTrek"
class='card mt-4' >
<div class='card-body'>
<h4>{{ selectedTrek.trek_name }}</h4>

<p>
<b>Location :</b>
{{ selectedTrek.location }}
</p>

<p>
<b>Assigned Staff :</b>
{{ selectedTrek.staff_name }}
</p>

<p>
<b>Difficulty :</b>
{{ selectedTrek.difficulty }}
</p>
<p>

<b>Duration :</b>
{{ selectedTrek.duration }} Days
</p>

<p>
<b>Description :</b >
{{ selectedTrek.description }}
</p>

<p>
<b>Available Slots :</b>
{{ selectedTrek.available_slots }}
</p>

<p>
<b>Status :</b>
{{ selectedTrek.status }}
</p>

<p>
<b>Start Date :</b >
{{ selectedTrek.start_date }}
</p>
<p>
<b>End Date : </b>
{{ selectedTrek.end_date }}
</p>

</div >
</div>
</div>
</template >

<script setup>
import { ref,computed,onMounted } from 'vue'
const trekList= ref([])
const selectedTrek = ref(null)
const search =ref("")
const durationFilter = ref("")
const difficultyFilter= ref("")
async function loadTreks(){
const response=await fetch( 
    'http://127.0.0.1:5000/trekker/treks',
{
    headers:{
        Authorization:
        "Bearer "+localStorage.getItem("token")
        }
    }
)

const data=await response.json()
if(!response.ok){
alert(data.message)
return
}
trekList.value=data
}

const filteredTreks = computed(() => {
    const keyword = search.value.toLowerCase()
    return trekList.value.filter(trek => {
        const matchesSearch =
            trek.trek_name.toLowerCase().includes(keyword) ||
            trek.location.toLowerCase().includes(keyword)
        const matchesDifficulty =
            difficultyFilter.value == "" ||
            trek.difficulty == difficultyFilter.value
        const matchesDuration =
            durationFilter.value == "" ||
            trek.duration == Number(durationFilter.value)
        return (
            matchesSearch &&
            matchesDifficulty &&
            matchesDuration
        )
    })
})

async function bookTrek(id){
const response=await fetch(
"http://127.0.0.1:5000/trekker/book/"+id,
{
    method:"POST",
    headers:{
        Authorization:
        "Bearer "+localStorage.getItem("token")
        }
        }
        )
const data=await response.json()
alert(data.message)
if(response.ok){
loadTreks()
}
}

async function viewDetails(id){
const response=await fetch(
    "http://127.0.0.1:5000/trekker/treks/"+id,
{
    headers:{
        Authorization:
        "Bearer "+localStorage.getItem("token")
        }
        }
        )
const data=await response.json()
if(!response.ok){
alert(data.message)
return
}
selectedTrek.value=data
}

onMounted(loadTreks)

</script>