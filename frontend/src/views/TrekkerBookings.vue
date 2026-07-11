<template>
<div class='container mt-4'>

<h2>My Bookings </h2 >

<button class='btn btn-primary mb-3' @click='loadBookings'> Refresh </button>
<RouterLink to="/trekker" class='btn btn-secondary mb-3 ms-2'> Back </RouterLink>

<table class='table table-bordered' >
<thead >
<tr >

<th>ID </th>
<th>Trek </th>
<th>Location </th>
<th>Difficulty </th>
<th>Booking Status </th >
<th> Trek Status </th >
<th>Date </th>
<th>Action </th >

</tr >
</thead >

<tbody>
<tr
v-for='booking in bookings'
:key='booking.booking_id'>

<td>{{ booking.booking_id }} </td>
<td>{{ booking.trek_name }} </td>
<td>{{ booking.location }} </td>
<td> {{ booking.difficulty }} </td>
<td>{{ booking.booking_status }} </td>
<td> {{ booking.trek_status }}</td >
<td>{{ booking.booking_date }} </td >
<td>
<button v-if="booking.booking_status=='BOOKED' && booking.trek_status=='OPEN'" class="btn btn-danger btn-sm"
@click="cancelBooking(booking.booking_id)">Cancel </button>
</td>

</tr>
</tbody>
</table>

</div>
</template>

<script setup >
import { ref,onMounted } from 'vue'
const bookings = ref([])
async function loadBookings(){
const response= await fetch(
    'http://127.0.0.1:5000/trekker/bookings',
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
bookings.value=data
}

async function cancelBooking(id){
    if(!confirm("Cancel Booking?")) return
    const response=await fetch(
        "http://127.0.0.1:5000/trekker/bookings/"+id,
        {
            method:"PUT",
            headers:{
                Authorization:
                "Bearer "+localStorage.getItem("token")
                }
        }
    )
const data=await response.json()
alert(data.message)
loadBookings()
}

onMounted(loadBookings)

</script>