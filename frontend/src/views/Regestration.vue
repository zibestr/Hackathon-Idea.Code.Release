<script setup>
import Line from '../Components/RegLine.vue'
import RegistrationBox from '../Components/RegBox.vue'
import IconStrelka from '../assets/icons/IconStrelka.vue'
</script>

<template>
<div class="reg_main">
    <div class="line">
        <Line />
    </div>
    <div class="strelka_div">
        <a href="/"><IconStrelka /></a>
    </div>
    <div class="reg_box_div">
        <RegistrationBox />
    </div>
</div>
</template>

<style scoped>
.reg_main {
    width: 100%;
}

.reg_box_div {
    display: flex;
    justify-content: center;
    margin-top: 110px;
    margin-bottom: 160px;
}
</style>
