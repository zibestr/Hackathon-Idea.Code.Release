# Проект Сервис поиска соседей для студентов

**[Презентация](https://docs.google.com/presentation/d/1th9iv3FWsIA2_Q-GjXGdMk18qkEOnsRDe4koc2GA4HM/edit?usp=sharing)**

## Развёртывание и запуск

### Добавление файла .env в корневую директорию проекта


### При проблемах с развертыванием на Unix системах

1. Stop Docker service

```sudo systemctl stop docker```

2. Change ownership of Docker socket

```sudo chown $USER:$USER /var/run/docker.sock```

3. Add your user to the docker group

```sudo usermod -aG docker $USER```

4. Restart Docker

```sudo systemctl start docker```

5. Apply group changes (or log out/in)

```newgrp docker```

6. Verify permissions

```ls -l /var/run/docker.sock```

Should show your username as owner if comands were executed correctly.



{
  "name": "sasha",
  "photos": [
  ],
  "gender": 0,
  "age": 52,
  "email": "aligos@yandex.ru",
  "phone": "+79897088242",
  "vk_id": "777",
  "region_name": "г. Москва",
  "locality_name": "г. Москва",
  "education_direction": "09.03.04",
  "educational_institution": "РТУ МИРЭА",
  "habits": [
    "Курение в помещении", "Частые жалобы"
  ],
  "interests": [
    "Создание косплея", "Йога"
  ],
  "budget": null,
  "about": "Я ЛЮБЛЮ МУЖЧИН",
  "hashed_password": "qwerty"
}