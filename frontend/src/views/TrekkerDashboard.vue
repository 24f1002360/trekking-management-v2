<template>
<div class="container mt-5">
<h2> Trekker Dashboard </h2 >
<p> Welcome Trekker </p>
<button class='btn btn-danger' @click='logout'>
Logout </button>

</div>
</template>
<script setup > 
function logout(){
    localStorage.clear()
    window.location='/'
}
</script>