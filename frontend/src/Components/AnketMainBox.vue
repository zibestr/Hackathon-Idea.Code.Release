<script setup>
import GenderChoice from '../Components/GenderChoice.vue'
const hender = [
    {value: 'Male', label: 'Мужской'},
    {value: 'Female', label: 'Женский'}
];
</script>

<template>
<div>
    <h2>Создание анкеты</h2>
    <div class="anket_input_div">
        <h3>ФИО</h3>
        <input class="name_input" placeholder="Иванов Иван Иванович">
    </div>
    <div class="anket_input_div">
        <h3>Пол</h3>
        <GenderChoice />
    </div>
    <div class="age_id_div"></div>
</div>
</template>

<style>

</style>