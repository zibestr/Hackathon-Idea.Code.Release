<script setup>
    import Line from '../Components/AuthLine.vue'
    import AuthBox from '../Components/AuthBox.vue'
    import IconStrelka from '../assets/icons/IconStrelka.vue'
</script>

<template>
<div class="auth_main">
    <div class="line">
        <Line />
    </div>
    <div class="strelka_div">
        <a href="/"><IconStrelka /></a>
    </div>
    <div class="auth_box_div">
        <AuthBox />
    </div>
</div>
</template>

<style scoped>
* {
    padding: 0;
    margin: 0;
}

.auth_main {
    width: 100%;
}

.line {
align-items: center;
display: flex;
justify-content: center;
width: 100%;
height: 100px;
}

.auth_box_div {
    display: flex;
    justify-content: center;
    margin-top: 110px;
    margin-bottom: 160px;
}
</style>