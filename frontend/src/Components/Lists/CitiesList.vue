<script>

export default {
    data() {
        return {
            cities: [
    {id: 1, city: "Москва"},
    {id: 2, city: "Москва 2"},
    {id: 3, city: "Москва 3"},
    {id: 4, city: "Москва 4"},
    {id: 5, city: "Москва 5"},
    {id: 6, city: "Москва 6"},
    {id: 7, city: "Москва 7"},
    {id: 8, city: "Москва 8"},
    {id: 9, city: "Москва 9"},
    {id: 10, city: "Москва 10"},
]
        }
    }
}
</script>

<template>
<div class="main_list_div">
    <div v-for="city in this.cities">
        <div class="city_text">
            <p>{{ city.city }}</p>
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
