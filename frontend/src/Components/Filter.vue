<script setup>

import Genders from '../Components/GenderChoice.vue'

</script>

<template>
<div class="filter_div">
    <h2>Фильтр</h2>
    <div>
    <Genders />
</div>
<div class="inputs_div">
<div class="anket_input_div">
    <h3>Возраст</h3>
    <input placeholder="">
</div>
<div class="anket_input_div">
    <h3>Направление обучения</h3>
    <input placeholder="">
</div>
<div class="anket_input_div">
    <h3>Интересы</h3>
    <input placeholder="">
</div>
<div class="anket_input_div">
    <h3>Вредные привычки</h3>
    <input placeholder="">
</div>
</div>
</div>
</template>

<style scoped>

.filter_div {
    width: 800px;
}

.input_div {
    width: 90%;
}
 
</style>
