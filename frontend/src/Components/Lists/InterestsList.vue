<script>

export default {
    data() {
        return {
            interests: [
    {id: 1, intrest: "Спорт"},
    {id: 2, intrest: "Спорт 2"},
    {id: 3, intrest: "Спорт 3"},
    {id: 4, intrest: "Спорт 4"},
    {id: 5, intrest: "Спорт 5"},
    {id: 6, intrest: "Спорт 6"},
    {id: 7, intrest: "Спорт 7"},
    {id: 8, intrest: "Спорт 8"},
    {id: 9, intrest: "Спорт 9"},
    {id: 10, intrest: "Спорт 10"},
]
        }
    }
}
</script>

<template>
<div class="main_list_div">
    <div v-for="interest in this.interests">
        <div class="city_text">
            <p>{{ interest.intrest }}</p>
    </div>
    </div>
</div>
</template>

<style>
.main_list_div {
    margin-top: 15px;
    width: 855px;
    height: 140px;
    border: 1px solid #000000;
    border-radius: 35px;
    padding: 20px 20px 30px 20px;
    overflow-y: auto;
}

.main_list_div {
  scrollbar-width: none; /* Для Firefox */
  -ms-overflow-style: none; /* Для IE/Edge */
}

.main_list_div::-webkit-scrollbar {
  display: none; /* Для Chrome/Safari/Opera */
}

.city_text {
    font-size: 24px;
    font-family: 'Mulish';
    margin-top: 1px;
}
</style>
