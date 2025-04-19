<script setup>
import IconStrelka from '../assets/icons/IconStrelka.vue'
import IconRightStrelka from '../assets/icons/IconRightStrelka.vue'

import Line from '../Components/RegLine.vue'
import MainAnketBox from '../Components/AnketMainBox.vue'
import NoHomeChioce from '../Components/NoHomeAnket.vue'
import HaveHomeChoice from '../Components/HaveHomeAnket.vue'

import CitiesList from '../Components/Lists/CitiesList.vue'
import RegionsList from '../Components/Lists/RegionsList.vue'
import LearnWaysList from '../Components/Lists/LearnWaysList.vue'
import InterestList from '../Components/Lists/InterestsList.vue'
import BadInterestsList from '../Components/Lists/BadInterestsList.vue'

import { LineStore } from '../stores/LineStates'

const store = LineStore();
</script>

<template>
<div class="anket_main">
    <div class="Line_div">
        <Line />
    </div>
    <div class="strelka_div">
        <a href="/regestration" @click="store.change_value('reg_second_line', false)"><IconStrelka /></a>
    </div>
    <div class="anket_position_2">
    <div class="anket_position">
    <div class="anket">
        <MainAnketBox />
    </div>
    <div class="age_vk_div">
        <div>
            <h3>Возраст</h3>
            <div class="age_input_div">
            <button class="sign_minus">-</button>
                <input placeholder="Возраст" class="age_input">
                <button class="sign_plus">+</button>
            </div>
        </div>
        <div class="vk_id_div">
            <h3>VK ID</h3>
            <input placeholder="VK ID">
        </div>
    </div>
    <div class="anket_input_div">
        <h3>Регион</h3>
        <div class="region_input">
            <input placeholder="Регион">
            <IconRightStrelka />
        </div>
        <div>
            <RegionsList /> 
        </div>
    </div>
    <div class="anket_input_div">
        <h3>Город</h3>
        <div class="region_input">
            <input placeholder="Город">
            <IconRightStrelka />
        </div>
        <div>
            <CitiesList />
        </div>
    </div>
    <div class="anket_input_div">
        <h3>Направление обучения</h3>
        <div class="region_input">
            <input placeholder="Направление обучения">
            <IconRightStrelka />
        </div>
        <div>
            <LearnWaysList />
        </div>
    </div>
    <div class="anket_input_div">
        <h3>Интересы</h3>
        <div class="region_input">
            <input placeholder="Интересы">
            <IconRightStrelka />
        </div>
        <div>
            <InterestList />
        </div>
    </div>
    <div class="anket_input_div">
        <h3>Вредные привычки</h3>
        <div class="region_input">
            <input placeholder="Вредные привычки">
            <IconRightStrelka />
        </div>
        <div>
            <BadInterestsList />
        </div>
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
    <div>
        <NoHomeChioce />
    </div>
    <div>
        <HaveHomeChoice />
    </div>
    <div class="anket_input_div">
        <h3>О себе</h3>
        <textarea placeholder="О себе" class="text_input">О себе</textarea>
    </div>
</div>
<a href="/" class="authreg_button" @click="store.change_value('reg_third_line', true)">Создать анкету</a>

</div>
</div>
</template>

<style scoped>
.anket_main {
    width: 100%;
    height: 100%;
    margin-bottom: 50px;
}

.anket {
    width: 100%;
    display: flex;
}

input {
    height: 40px;
    margin-top: 0px;
}

.age_vk_div {
    height: 100px;
    width: 100%;
    display: flex;
    align-items: center;
    flex-direction: row;
    gap: 116px;
}

.age_input_div {
    position: relative;
    width: 266px;
}

.vk_id_div {
    margin-top: 40px;
}

.vk_id_div input {
    width: 251px;
    padding: 0;
    padding-left: 15px;
}

.sign_minus {
    position: absolute;
    background-color: transparent;
    margin: 6px;
    margin-left: 15px;
    height: 30px;
    width: 30px;
    border: 0px;
    font-size: 24px;
    z-index: 10;
}

.sign_plus {
    position: absolute;
    background-color: transparent;
    margin: 6px;
    height: 30px;
    width: 30px;
    border: 0px;
    right: 17px;
    font-size: 24px;
    z-index: 10;
}

.age_input {
    position: absolute;
    margin-top: 0px;
    z-index: 0;
    text-align: center;
    width: 266px;
    padding: 0px;
}

.region_input {
    display: flex;
    align-items: center;
    position: relative;
    width: 919px;
}

.region_input input {
    width: 919px;
    margin-top: 5px;
}

svg {
    top: 5px;
    position: relative;
    right: 40px;
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
}

.indicator_dot {
    width: 20px;
    height: 20px;
    border: 1px solid #000000;
    border-radius: 50%;
    background-color: #ffffff;
}

.text_input {
    width: 916px;
    height: 112px;
    border: 1px solid #000000;
    border-radius: 35px;
    resize: none;
    padding: 15px;

    font-size: 18px;
    font-family: "Mulish";
}

.anket_position {
    width: 920px;
}

.anket_position_2 {
    display: flex;
    flex-direction: column;
    align-content: center;
    flex-wrap: wrap;
    align-items: center;
}

.anket_input_div {
    width: 100%;
}
</style>
