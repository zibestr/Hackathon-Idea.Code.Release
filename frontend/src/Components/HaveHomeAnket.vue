<script setup>
import { ref } from 'vue';

const fileInput = ref(null);
const fileName = ref('');

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  fileName.value = file ? file.name : '';
};
</script>

<template>
<div>
    <div class="anket_input_div">
        <h3>Фото жилья</h3>
        <div>
            <div class="file-upload-container">
    <input
      type="file"
      ref="fileInput"
      @change="handleFileChange"
      class="file-input"
    />
    <div 
      class="file-upload-button"
      @click="triggerFileInput"
    >
      {{ fileName || 'Добавить файл' }}
    </div>
  </div>
        </div>
    </div>
    <div class="anket_input_div">
        <h3>Стоимость аренды</h3>
        <input placeholder="Стоимость">
    </div>
    <div class="anket_input_div">
        <h3>Условия съема</h3>
        <input class="long_input"  placeholder="Условия">
    </div>
    <div class="anket_input_div">
        <h3>Ссылка на объявление</h3>
        <input class="long_input" placeholder="Ссылка">
    </div>
</div>
</template>

<style>
.long_input {
    width: 916px;
}

.file-upload-container {
  position: relative;
  display: inline-block;
}

.file-input {
  display: none;
}

.file-upload-button {
    width: 266px;
    height: 40px;
    line-height: 30px;
    text-align: center;
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 35px;
    cursor: pointer;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    padding: 0 8px;
    transition: border-color 0.3s;
    display: flex;
    align-content: center;
    justify-content: center;
    flex-wrap: wrap;

  font-family: 'Mulish';
  font-size: 20px;
}
</style>