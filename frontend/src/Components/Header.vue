<script setup>
import "@fontsource/mulish";
import { LineStore } from "../stores/LineStates";

const store = LineStore()
</script>

<template>
<div class="header">
    <div class="name">
        <div>
        <svg width="50" height="50" viewBox="0 0 50 50" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M11.858 0.146484C11.4968 0.312469 11.0769 0.751835 10.9402 1.11309C10.8621 1.30837 10.8328 8.51399 10.8328 24.8682V48.3402H5.69713H0.561414L0.278266 48.6233C-0.0927553 48.9943 -0.0927553 49.3458 0.278266 49.7169L0.561414 50H24.9902H49.419L49.7022 49.7169C49.8682 49.5411 49.9853 49.3263 49.9853 49.1701C49.9853 49.0139 49.8682 48.7991 49.7022 48.6233L49.419 48.3402H44.2833H39.1476V24.8682C39.1476 8.51399 39.1183 1.30837 39.0402 1.11309C38.9035 0.742073 38.4837 0.302704 38.1029 0.146484C37.644 -0.0487862 12.2974 -0.0487862 11.858 0.146484ZM37.4878 25.0049V48.3402H36.6579H35.8279V26.489C35.8279 5.39936 35.8182 4.62803 35.6424 4.30583C35.5448 4.12032 35.3007 3.83717 35.1054 3.67118L34.7344 3.37827H24.9902H15.246L14.875 3.67118C14.6797 3.83717 14.4356 4.12032 14.338 4.30583C14.1623 4.62803 14.1525 5.39936 14.1525 26.489V48.3402H13.3226H12.4927V25.0049V1.66962H24.9902H37.4878V25.0049ZM34.1681 17.1158V29.2521H33.3382H32.518L32.4888 21.0994L32.4497 12.9467L32.2349 12.2144C31.5319 9.91996 30.0576 8.23084 27.9584 7.30329C26.1521 6.50266 23.8283 6.50266 22.0221 7.30329C19.9229 8.23084 18.4485 9.91996 17.7455 12.2144L17.5307 12.9467L17.4917 21.4802C17.4722 28.0121 17.4917 30.0918 17.5796 30.3066C17.8139 30.8631 17.7553 30.8631 24.6192 30.8631H30.8973V31.693V32.523H24.4435H17.9896L17.7553 32.7768L17.521 33.0307V39.6114V46.1824L17.7455 46.407L17.9701 46.6315H24.9902H32.0103L32.2349 46.407L32.4595 46.1824L32.4888 40.1582L32.5083 34.134L33.3382 34.1242H34.1681V41.2322V48.3402H24.9902H15.8123V26.6647V4.98929H24.9902H34.1681V17.1158ZM26.5524 8.57257C28.4661 9.09981 29.999 10.6425 30.6239 12.6538C30.7899 13.2006 30.7996 13.7473 30.7996 21.1971V29.1545H24.9902H19.1808V21.1971C19.1808 13.7473 19.1906 13.2006 19.3566 12.6538C20.0693 10.3496 21.9439 8.6995 24.2091 8.39682C24.8926 8.30895 25.8592 8.3773 26.5524 8.57257ZM33.7873 30.9901C34.422 31.4782 34.1291 32.4644 33.3382 32.4644C32.5962 32.4644 32.2349 31.6149 32.7524 31.1072C33.016 30.8436 33.5237 30.785 33.7873 30.9901ZM30.8485 39.6016V45.0205H24.9902H19.132V39.6016V34.1828H24.9902H30.8485V39.6016Z" fill="black"/>
        </svg>
        <h1>TheN</h1>
        </div>
    </div>
    <div class="input_button">
        <a href="/auth" @click="store.change_auth_value(false)">Войти</a>
    </div>
</div>
</template>

<style scoped>

* {
    margin: 0;
    padding: 0;
}

.header {
    position: relative;
    width: 100%;
    height: 60px;
    background-color: white;
}

.name {
    position: relative;
    margin-left: 40px;
    margin-top: 10px;
    width: 150px;
    height: 60px;
    text-align: center;
    display: inline-block;
}
.name svg {
    height: 50px;
    position: absolute;
    top: 0;
    left: 0;
}

.name h1 {
    position: relative;
    left: 25px;
    padding-top: 10px;
    height: 50px;

    font-family: 'Mulish';
    font-style: normal;
    font-weight: 200;
    font-size: 40px;
    line-height: 50px;

color: #000000;
}

.input_button {
    position: absolute;
    top: 16px;
    right: 40px;
}

.input_button a {
    width: 130px;
    height: 34px;
    border: 1px solid #000000;
    border-radius: 45px;
    text-align: center;
    text-decoration: none;
    font-family: 'Mulish';
    font-style: normal;
    font-weight: 400;
    font-size: 20px;
    line-height: 25px;
    display: flex;
    align-items: center;
    justify-content: center;

color: #000000;
}
</style>
