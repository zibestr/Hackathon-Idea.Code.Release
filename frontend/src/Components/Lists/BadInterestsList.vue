<script>

export default {
    data() {
        return {
            bad_interests: [
    {id: 1, bad_intrest: "Курение"},
    {id: 2, bad_intrest: "Курение 2"},
    {id: 3, bad_intrest: "Курение 3"},
    {id: 4, bad_intrest: "Курение 4"},
    {id: 5, bad_intrest: "Курение 5"},
    {id: 6, bad_intrest: "Курение 6"},
    {id: 7, bad_intrest: "Курение 7"},
    {id: 8, bad_intrest: "Курение 8"},
    {id: 9, bad_intrest: "Курение 9"},
    {id: 10, bad_intrest: "Курение 10"},
]
        }
    }
}
</script>

<template>
<div class="main_list_div">
    <div v-for="bad_interest in this.bad_interests">
        <div class="city_text">
            <p>{{ bad_interest.bad_intrest }}</p>
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
