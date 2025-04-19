<script>

export default {
    data() {
        return {
            Ways: [
    {id: 1, way: "09.03.01"},
    {id: 2, way: "09.03.02"},
    {id: 3, way: "09.03.03"},
    {id: 4, way: "09.03.04"},
    {id: 5, way: "09.03.05"},
    {id: 6, way: "09.03.06"},
    {id: 7, way: "09.03.07"},
    {id: 8, way: "09.03.08"},
    {id: 9, way: "09.03.09"},
    {id: 10, way: "09.03.10"},
]
        }
    }
}
</script>

<template>
<div class="main_list_div">
    <div v-for="way in this.Ways">
        <div class="city_text">
            <p>{{ way.way }}</p>
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
