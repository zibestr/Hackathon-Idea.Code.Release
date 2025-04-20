<script setup>
import ProfileHaveHome from '../Components/PrfileHaveHome.vue'
import Photos from '../Components/ProfilePhotos.vue'
import ProfileHaveMoney from '../Components/PrfileMoney.vue'

import IconLocation from '../assets/icons/IconLocation.vue';
import IconEducation from '../assets/icons/IconEducation.vue';
</script>

<template>
<div class="main_div">
    <div class="photo_div">
        <h2>Профиль</h2>
        <img class="profile_img" src="../assets/standart_profile.jpg">
        <div class="home_status">
            <p>Есть жилье</p>
        </div>
        <a>Редактировать</a>
    </div>
    <div class="main_info_div">
        <h2>Полина Игнатова</h2>
        <p>18 лет</p>
        <p>VK: </p>
        <div class="about">
            <p>О себе:</p>
            <p>Люблю путешествовать, изучать культуры и пробовать разные кухни. В свободное время увлекаюсь чтением и занятиями спортом. Моя жизнь — это постоянное самосовершенствование и стремление к новым вершинам.</p>
        </div>
        <div class="info_components">
            <div class="small_components">
                <div class="small_component">
                    <IconLocation />
                    <p>Москва</p>
                </div>
                <div class="small_component">
                    <IconEducation />
                    <p>Программная инженерия</p>
                </div>
            </div>
            <div class="photos">
                <Photos />
            </div>
            <div class="big_components">
                <div class="big_component">
                    <h2>Интересы</h2>
                    <div class="interests_list">
                        <p>Спорт</p>
                        <p>Программирование</p>
                        <p>Хардбасс</p>
                    </div>
                </div>
                <div class="big_component">
                    <h2>Вредные привычки</h2>
                    <div class="interests_list">
                        <p>Курить</p>
                        <p>Развожу тараканов</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="room">
            <ProfileHaveHome />
        </div>
        <div class="money">
            <ProfileHaveMoney />
        </div>
    </div>
</div>
</template>
<style>
.main_div {
    margin-left: 150px;
    margin-right: 110px;
    display: flex;
    flex-direction: row;
    gap: 60px;
}

.photo_div {
    width: 250px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.photo_div p {
    text-align: center;
    border-bottom: 1px solid #FF5E37;
    margin-bottom: 30px;
}

.photo_div a {
    border: 1px solid #000;
    width: 250px;
    height: 45px;
    border-radius: 35px;
    display: flex;
    align-items: center;
    justify-content: center;

    font-family: 'Mulish';
    font-size: 20px;
    text-decoration: none;
}

.home_status {
    width: 200px;
}

.home_status p {
    font-family: 'Mulish';
    font-size: 32px;
}

.profile_img {
    width: 250px;
    height: 250px;
    border-radius: 50%;

    margin-top: 30px;
    margin-bottom: 30px;
    object-fit: cover;
    object-position: top;
}

.main_info_div p {
    font-family: 'Mulish';
    font-size: 32px;
}

.about {
    display: flex;
    flex-direction: row;
}

.about p {
    min-width: 120px;
}

.info_components {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.small_components {
    margin-top: 30px;
    display: flex;
    flex-direction: row;
    gap: 30px;
}

.small_component {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.photos {
    margin: 30px;
}

.big_components {
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 60px;
}

.big_component {
    width: 440px;
    height: 300px;
    border: 1px solid #000;
    border-radius: 35px;
    padding: 15px;
}

.big_component h2 {
    font-size: 40px;
    font-weight: 300;
    border-bottom: 1px solid #FF5E37;
}

.interests_list {
    margin-top: 30px;
    display: flex;
    flex-direction: column
}
.interests_list p {
    margin-top: 5px;
}

.room {
    margin: 30px;
}
</style>