<template>
<div class='container mt-4'>
<h2> Booking Records </h2>
<button class='btn btn-primary mb-3' @click='loadStaff'> Refresh </button>
<RouterLink to="/admin" class="btn btn-secondary mb-3 ms-2"> Back </RouterLink>

<table class='table table-bordered'>
<thead>
<tr>
<th>ID </th >
<th> User </th>
<th> Trek </th >
<th> Booking Status </th>
<th> Trek Status </th>
<th> Booking Date </th>
<th> Completed Date </th>
</tr>
</thead>

<tbody>
<tr v-for='booking in bookingList' :key='booking.booking_id'>
<td>{{ booking.booking_id }}</td>
<td> {{ booking.user_name }}</td>
<td> {{ booking.trek_name }}</td >
<td> {{ booking.booking_status }}</td>
<td> {{ booking.trek_status }}</td>
<td> {{ booking.booking_date }}</td>
<td> {{ booking.completed_date }}</td>
</tr>
</tbody>
</table>
</div >
</template>

<script setup>
import {ref , onMounted} from 'vue'
const bookingList = ref([])
async function loadBookings(){
    const response=await fetch('http://127.0.0.1:5000/admin/bookings',
    {headers:{Authorization:'Bearer '+localStorage.getItem('token')}})
    bookingList.value = await response.json()
}
onMounted(loadBookings)
</script>

