<script>

export default {
    data() {
        return {
            instituts: [
    {id: 1, institut: "РТУ МИРЭА"},
    {id: 2, institut: "РТУ МИРЭА 2"},
    {id: 3, institut: "РТУ МИРЭА 3"},
    {id: 4, institut: "РТУ МИРЭА 4"},
    {id: 5, institut: "РТУ МИРЭА 5"},
    {id: 6, institut: "РТУ МИРЭА 6"},
    {id: 7, institut: "РТУ МИРЭА 7"},
    {id: 8, institut: "РТУ МИРЭА 8"},
    {id: 9, institut: "РТУ МИРЭА 9"},
    {id: 10, institut: "РТУ МИРЭА 10"},
]
        }
    }
}
</script>

<template>
<div class="main_list_div">
    <div v-for="institut in this.instituts">
        <div class="city_text">
            <p>{{ institut.institut }}</p>
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
