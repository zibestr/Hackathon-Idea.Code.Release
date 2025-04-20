<script setup>
import IconElipsis from '../assets/icons/IconElipsis.vue';
</script>

<template>
<div class="person_row">
    <div class="img_name_div">
    <div class="person_img">
        <img src="../assets/women2.jpg">
    </div>
    <div class="person_name">
        <h3>Ирина Гордеева</h3>
</div>
</div>
    <div class="person_actions">
    <div class="person_button">
        <button class="authreg_button">Принять</button>
    </div>
    <div class="person_icon">
        <IconElipsis />
    </div>
</div>
</div>
</template>

<style>
.person_row {
    width: 1144px;
    height: 113px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    box-sizing: border-box;
    background-color: #D3D3D3;
    border-radius: 35px;
}

.person_actions {
    position: relative;
    right: 0px;
    display: flex;
    flex-direction: row;
    align-items: center;
}

.person_name h3 {
    margin: 0px;
    margin-left: 20px;
}

.person_icon {
    display: flex;
    align-items: center;
}

.person_img img {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    object-fit: cover;
    object-position: top;
}

.img_name_div {
    display: flex;
    align-items: center;
    justify-content: center;
}

.person_name {
    font-size: 32px;
}

.person_button button {
    margin-top: 0px;
    margin-right: 40px;
}
</style>