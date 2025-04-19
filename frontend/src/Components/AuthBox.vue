<script setup>

import { LineStore } from '../stores/LineStates';

const store = LineStore()

const SetLines = () => {
    store.change_value('reg_second_line', false);
    store.change_value('reg_third_line', false);
}

</script>

<template>
<div class="auth_div">
    <div class="head_div">
        <h2 class="auth_head">Вход</h2>
    </div>
    <div class="input_div">
    <input class="auth_input" placeholder="Логин">
    <input class="auth_input" placeholder="Пароль">
    <a class="authreg_button" href="/" @click="store.change_auth_value(true)">Войти</a>
    <div class="to_reg">
        <p>Нет аккаунта?</p>
        <a href="/regestration" @click="SetLines">Зарегистрироваться</a>
    </div>
    </div>
</div>
</template>

<style scoped>
.auth_div {
    position: relative;
    width: 620px;
    height: 482px;
    background-color: #FFFFFF;
    border: 1px solid #000000;
    border-radius: 35px;
}
</style>
