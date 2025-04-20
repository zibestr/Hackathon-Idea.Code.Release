<script>

export default {
    data() {
        return {
            male_choice: false,
            female_choice: false
        }
    },
    methods: {
        SetMale() {
            this.male_choice = true;
            this.female_choice = false;
        },
        SetFemale() {
            this.male_choice = false;
            this.female_choice = true;
        }
    }
}

</script>

<template>
<div class="gender_div">
    <button @click="SetMale()">
        <div v-if="this.male_choice == true" class="selected_indicator_dot"></div>
        <div v-else class="indicator_dot"></div>
        <div>
        <p>Мужской</p>
    </div>
    </button>
    <button @click="SetFemale()">
        <div v-if="this.female_choice == true" class="selected_indicator_dot"></div>
        <div v-else class="indicator_dot"></div>
        <div>
        <p>Женский</p>
    </div>
    </button>
</div>
</template>
  
<style scoped>
.gender_div {
    margin-top: 10px;
    width: 100%;
    display: flex;
    flex-direction: row;
    gap: 116px;
}

button {
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 12px;
    padding: 0 26px;

    border-radius: 35px;
    width: 266px;
    height: 40px;
    border: 1px solid #000000;
    background-color: white;

    position: relative;
}

.indicator_dot {
    width: 20px;
    height: 20px;
    border: 1px solid #000000;
    border-radius: 50%;
    background-color: #ffffff;
}

.selected_indicator_dot {
    width: 20px;
    height: 20px;
    border: 1px solid #000000;
    border-radius: 50%;
    background-color: #FF5E37;
}


p {
    font-size: 20px;
    font-family: 'Mulish';
    color: #000000;

    flex: 1; /* Занимает всё доступное пространство */
  text-align: center; /* Выравнивание текста */
  margin-right: 26px; /* Компенсируем padding кнопки */
}
</style>