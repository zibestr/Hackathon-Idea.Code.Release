<script setup>

</script>

<template>
<div class="gender_div">
    <button>
        <div class="indicator_dot"></div>
        <div>
        <p>Мужской</p>
    </div>
    </button>
    <button>
        <div class="indicator_dot"></div>
        Женский
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


p {
    flex: 1; /* Занимает всё доступное пространство */
  text-align: center; /* Выравнивание текста */
  margin-right: 26px; /* Компенсируем padding кнопки */
}
</style>