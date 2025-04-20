<script setup>
import IconLocation from '../assets/icons/IconLocation.vue';
import IconEducation from '../assets/icons/IconEducation.vue';

import HomeRec from '../Components/RecHome.vue'
</script>

<script>

export default {
    data() {
        return {
            good_interests: ['Спорт', 'Книги', 'Игры'],
            bad_interests: ['Храп', 'Алкоголь']
        }
    }
}

</script>

<template>
<div class="person_div">
    <img src="../assets/man1.jpg">
    <div class="person_inf_div">
    <h1>Евгений Сидоров</h1>
    <p>20 лет</p>
    <div class="small_element">
        <IconLocation />
        <p>Нижний Новгород</p>
    </div>
    <div class="small_element">
        <IconEducation />
        <p>Менеджмент</p>
    </div>
    <div class="all_interests">
    <div class="interests">
        <p>Интересы:</p>
        <div class="interests_list">
        <div v-for="(interest, index) in this.good_interests">
            <p class="interest_item">{{ interest }}</p>
        </div>
    </div>
    </div>
    <div class="interests">
        <p>Вредные привычки:</p>
        <div class="interests_list">
        <div v-for="(interest, index) in this.bad_interests">
            <p class="interest_item">{{ interest }}</p>
        </div>
    </div>
</div>
</div>
    </div>
    <div class="home">
        <HomeRec />
    </div>
</div>
</template>

<style>
.person_div {
    width: 700px;
    border: 1px solid #000;
    border-radius: 35px;
    display: inline-flex;
    flex-direction: column;
    align-items: center;

}

.person_div img {
    width: 100%;
    height: 440px;
    border-radius: 35px;
    object-fit: cover;
    object-position: top;
}

.person_div h1 {
    font-size: 48px;
    font-family: 'Mulish';
}

.person_div p {
    font-size: 32px;
    font-family: 'Mulish';
}

.person_inf_div {
    width: 90%;
}

.small_element {
    display: flex;
    flex-direction: row;
    gap: 10px;
}

.svg_size {
    width: 40px;
    height: 40px;
}

.interests {
    display: inline-flex;
    flex-direction: row;
    align-items: center;
    height: 30px;
    border: 1px solid #000;
    border-radius: 35px;
    padding: 10px;
}

.interests p {
    font-size: 20px;
    margin-right: 10px;
    margin-top: 0px;
}

.interests_list {
    display: flex;
    flex-direction: row;
    gap: 5px;
    margin: 0px;
}

.all_interests {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 15px;
    width: 100%;
}

.home p{
    font-size: 28px;
}
</style>