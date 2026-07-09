<template>
<div class="container mt-5" >
<h2> Staff Dashboard </h2 >
<p> Welcome Trek Staff </p>
<button class='btn btn-danger' @click='logout'>
Logout </button>

</div>
</template>
<script setup>
function logout(){
    localStorage.clear()
    window.location='/'
}
</script >