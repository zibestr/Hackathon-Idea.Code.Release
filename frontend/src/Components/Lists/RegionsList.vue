<script>

export default {
    data() {
        return {
            regions: [
    {id: 1, region: "Красногорск"},
    {id: 2, region: "Красногорск 2"},
    {id: 3, region: "Красногорск 3"},
    {id: 4, region: "Красногорск 4"},
    {id: 5, region: "Красногорск 5"},
    {id: 6, region: "Красногорск 6"},
    {id: 7, region: "Красногорск 7"},
    {id: 8, region: "Красногорск 8"},
    {id: 9, region: "Красногорск 9"},
    {id: 10, region: "Красногорск 10"},
]
        }
    }
}
</script>

<template>
<div class="main_list_div">
    <div v-for="region in this.regions">
        <div class="city_text">
            <p>{{ region.region }}</p>
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
