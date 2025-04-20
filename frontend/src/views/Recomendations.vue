<script setup>
import PersonRec from '../Components/RecPerson.vue'
import Filter from '../Components/Filter.vue'
</script>

<template>
<div class="rec_div">
    <!--<div class="filter_div">
        <Filter />
    </div> -->
    <PersonRec />
    <div class="buttons_div">
        <div class="no_button_position">
    <button class="no_button">Нет</button>
</div>
<div class="yes_button_position">
    <button class="yes_button">Да</button>
</div>
</div>
</div>
</template>

<style>
.rec_div {
    width: 100%;
    display: flex;
    align-items: center;
    flex-direction: column;
    margin-top: 80px;
    margin-bottom: 80px;
}

.buttons_div {
    margin-top: 15px;
    width: 640px;
    display: flex;
    flex-direction: row;
}

.no_button {
    width: 180px;
    height: 60px;
    border: 1px solid #000;
    border-radius: 35px;
    background-color: #fff;

    font-family: 'Mulish';
    font-size: 28px;
}

.yes_button {
    position: relative;
    right: 0px;
    width: 180px;
    height: 60px;
    border: 1px solid #000;
    border-radius: 35px;
    background-color: #FF5E37;

    font-family: 'Mulish';
    font-size: 28px;
}

.yes_button_position {
    width: 100%;
    display: flex;
    justify-content: flex-end
}
</style>