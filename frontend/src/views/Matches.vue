<script setup>
import Person from '../Components/PersonMatch.vue'
</script>

<template>
<div class="match_div">
    <div class='match_element_div'>
    <h2>Входящие</h2>
    <div class="matches">
    <div>
        <Person />
    </div>
</div>
</div>
</div>
</template>

<style>
.matches {
    display: flex;
    justify-content: center;
    margin-top: 30px;
    margin-bottom: 50px;
}

.match_div {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.match_element_div {
    width: 90%;
}
</style>