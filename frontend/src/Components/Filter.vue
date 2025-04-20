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
    <input placeholder="" class="long_input">
</div>
<div class="anket_input_div">
    <h3>Интересы</h3>
    <input placeholder="" class="long_input">
</div>
<div class="anket_input_div">
    <h3>Вредные привычки</h3>
    <input placeholder="" class="long_input">
</div>
<div class="house_div">
        <h3>Жилье</h3>
        <button>
        <div class="indicator_dot"></div>
        <div>
            <p>Есть жилье</p>
        </div>
        </button>
        <button>
        <div class="indicator_dot"></div>
        <div>
        <p>В поиске</p>
        </div>
        </button>
    </div>
</div>
</div>
</template>

<style scoped>

.filter_div {
    width: 700px;
    height: 100%;
    background-color: #fff;
    padding: 50px;
}

.input_div {
    width: 90%;
}
 

 .long_input {
    width: 644px;
 }

 .house_div {
    margin-top: 10px;
    width: 100%;
    display: flex;
    flex-direction: column;
}

.house_div button {
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-top: 5px;
    padding: 0 26px;

    border-radius: 35px;
    width: 266px;
    height: 40px;
    border: 1px solid #000000;
    background-color: white;

    position: relative;
}

.house_div p {
    margin-left: 10px;

    font-family: 'Mulish';
    font-size: 20px;
}

.indicator_dot {
    width: 20px;
    height: 20px;
    border: 1px solid #000000;
    border-radius: 50%;
    background-color: #ffffff;
}
</style>
