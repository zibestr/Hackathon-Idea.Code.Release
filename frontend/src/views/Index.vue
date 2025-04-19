<script>

</script>

<template>
<div class="main">
    <img src="../assets/main_image.png" class="image">
    <h1>The Neighborhood</h1>
    <p>Сервис поиска людей</p>
    <a>Найти соседа</a>
</div>
</template>

<style scoped>
* {
    padding: 0;
    margin: 0;
}

.main {
    width: 100%;
    min-height: 967px;
}

.image {
    position: absolute;
    right: 0;
    z-index: -10;
}

.main h1 {

    width: 1132px;
    height: 161px;

    font-family: 'Mulish';
    font-style: normal;
    font-weight: 700;
    font-size: 128px;
    line-height: 161px;
    background-color: white;

    position: relative;
    top: 79px;
    left: 40px;

color: #000000;
}

.main p {
    position: relative;
    width: 553px;
    height: 40px;
    left: 40px;
    top: 105px;

    font-family: 'Mulish';
    font-style: normal;
    font-weight: 500;
    font-size: 32px;
    line-height: 40px;

    color: #000000;
}


.main a {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    
    width: 346px;
    height: 60px;
    left: 40px;
    top: 204px;

    background: #FF5E37;
    border-radius: 45px;

    font-family: 'Mulish';
    font-style: normal;
    font-weight: 700;
    font-size: 24px;
    line-height: 30px;

color: #000000;



}
</style>
