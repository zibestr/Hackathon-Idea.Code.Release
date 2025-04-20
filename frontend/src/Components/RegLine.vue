<script setup>
import { LineStore } from '../stores/LineStates';

const store = LineStore();

</script>

<template>
<div class="main_line">
    <div class="full_line">
    </div>
    <div class="point">
        <p>1</p>
    </div>
    <div v-if="store.reg_line.reg_second_line == true" class="full_line">
    </div>
    <div v-else class="empty_line">
    </div>
    <div class="point">
        <p>2</p>
    </div>
    <div v-if="store.reg_line.reg_third_line == true" class="full_line"></div>
    <div v-else class="empty_line"></div>
</div>
</template>

<style>
* {
    padding: 0;
    margin: 0;
}

.main_line {
    display: flex;
    width: 95%;
    height: 34px;
    margin: 20px;
    text-align: center;
    align-items: center; /* Выравниваем элементы по вертикали */
    flex-direction: row;   /* Элементы в строку (по умолчанию) */
    gap: 8px; /* Расстояние между элементами */
}

.full_line {
    flex: 1;
    height: 14px;
    min-width: 20px;
    border: 1px solid #FF5E37;
    background-color: #FF5E37;
    border-radius: 35px;
}

.empty_line {
    flex: 1;
    height: 14px;
    min-width: 20px;
    border: 1px solid #FF5E37;
    border-radius: 35px;
}

.point {
    width: 34px;
    height: 34px;
    background-color: #FF5E37;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Mulish';
    font-style: normal;
    font-weight: 500;
    font-size: 20px;
    line-height: 25px;

color: #FFFFFF;


}
</style>