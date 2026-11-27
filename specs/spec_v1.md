# Módulo: Cuentas de jugador y sesión

## 1. Contexto y alcance

El RPG Manager es un sistema de consola para administrar personajes de rol. Este módulo permite que una persona se registre con una cuenta, inicie y cierre sesión, recupere su contraseña y asocie personajes a su cuenta. Queda fuera de alcance la creación, edición y eliminación de personajes (de eso se ocupa otro módulo), el envío real de correos electrónicos, la autenticación de dos factores y el inicio de sesión con redes sociales. Este módulo define su propia versión mínima de Personaje, con solo nombre y clase.

## 2. Actores

- **Visitante**: persona que todavía no tiene sesión iniciada; quiere registrarse o recuperar su contraseña.
- **Jugador**: persona con una cuenta registrada que usa el sistema para administrar sus personajes.

## 3. Requerimientos funcionales

- **RF-01** El visitante puede registrar una cuenta indicando nombre de usuario, correo electrónico y contraseña.
  - Criterio de aceptación: con datos que cumplen RN-01, RN-02 y RN-03, el sistema crea la cuenta en estado Activa, con 0 personajes y 0 intentos fallidos; si algún dato incumple una regla, no se crea la cuenta y el mensaje indica la regla violada.
- **RF-02** El jugador puede iniciar sesión con su nombre de usuario y su contraseña.
  - Criterio de aceptación: con credenciales correctas y cuenta no bloqueada, el sistema crea una sesión activa asociada a la cuenta y pone en 0 el contador de intentos fallidos; con credenciales incorrectas no crea sesión y el contador aumenta en 1 según RN-04.
- **RF-03** El jugador puede cerrar su sesión.
  - Criterio de aceptación: tras cerrar la sesión, su estado es Cerrada y cualquier consulta de perfil o de personajes con esa sesión es rechazada.
- **RF-04** El jugador con sesión activa puede consultar su perfil.
  - Criterio de aceptación: el perfil muestra nombre de usuario, correo, fecha de registro y cantidad de personajes de la cuenta; no muestra la contraseña.
- **RF-05** El visitante puede solicitar la recuperación de su contraseña indicando su correo electrónico.
  - Criterio de aceptación: si el correo pertenece a una cuenta, el sistema genera un token de recuperación que cumple RN-07; la respuesta al visitante es la misma exista o no el correo, según RN-08.
- **RF-06** El visitante puede restablecer su contraseña presentando un token de recuperación y una contraseña nueva.
  - Criterio de aceptación: con un token vigente y no usado y una contraseña nueva que cumple RN-02, el sistema cambia la contraseña, marca el token como usado, pone el contador de intentos fallidos en 0, desbloquea la cuenta y cierra sus sesiones activas; si el token está vencido o ya usado, no cambia nada.
- **RF-07** El jugador con sesión activa puede asociar un personaje a su cuenta indicando el nombre y la clase del personaje (Guerrero, Mago o Arquero).
  - Criterio de aceptación: si la cuenta tiene menos personajes que el máximo de RN-05, la cantidad de personajes de la cuenta aumenta en 1 y el personaje aparece en su lista; si ya alcanzó el máximo, el sistema rechaza la asociación y no cambia la lista.
- **RF-08** El jugador con sesión activa puede listar los personajes de su cuenta.
  - Criterio de aceptación: la lista muestra el nombre y la clase de cada personaje asociado a su cuenta y ningún personaje de otra cuenta.

## 4. Requerimientos no funcionales

- **RNF-01** Las contraseñas se guardan solo como hash con sal, con un costo de al menos 10 en bcrypt; ninguna contraseña se guarda en texto plano.
- **RNF-02** El inicio de sesión responde en menos de 2 segundos con hasta 10000 cuentas registradas.
- **RNF-03** Las reglas de negocio de este módulo tienen pruebas unitarias con al menos 70 % de cobertura.
- **RNF-04** El 100 % de los mensajes de error en español indica el código de la regla de negocio violada (por ejemplo, RN-01).

## 5. Reglas de negocio

- **RN-01** El nombre de usuario es único sin distinguir mayúsculas de minúsculas, tiene entre 4 y 20 caracteres y solo contiene letras y dígitos.
- **RN-02** La contraseña tiene al menos 8 caracteres, con al menos una mayúscula, una minúscula y un dígito, y no puede ser igual al nombre de usuario.
- **RN-03** El correo electrónico es único en el sistema y tiene el formato texto@dominio.
- **RN-04** Tras 5 intentos fallidos consecutivos de inicio de sesión, la cuenta pasa a estado Bloqueada durante 15 minutos; mientras está bloqueada no se puede iniciar sesión aunque la contraseña sea correcta.
- **RN-05** Una cuenta puede tener como máximo 3 personajes asociados.
- **RN-06** Un personaje pertenece a una sola cuenta.
- **RN-07** Un token de recuperación es válido durante 30 minutos desde su creación y se puede usar una sola vez; al generar un token nuevo para una cuenta, el anterior deja de ser válido.
- **RN-08** Los mensajes del sistema no revelan si el nombre de usuario o el correo existen: ante credenciales inválidas se muestra el mismo mensaje sin importar cuál dato falló.
- **RN-09** Una sesión sin actividad durante 30 minutos pasa a estado Cerrada.

## 6. Supuestos y glosario

- **Cuenta**: registro de un jugador con nombre de usuario, correo, contraseña (como hash), estado (Activa o Bloqueada), contador de intentos fallidos y fecha de registro.
- **Sesión**: periodo en que un jugador está autenticado; tiene estado Activa o Cerrada y fecha del último movimiento.
- **Intento fallido consecutivo**: inicio de sesión con credenciales incorrectas sin ningún inicio correcto en medio.
- **Token de recuperación**: código de un solo uso, con fecha de creación y estado (usado o no usado), que permite restablecer la contraseña. Se asume que el sistema lo muestra en consola en lugar de enviarlo por correo.
- **Personaje**: en este módulo, solo un nombre y una clase (Guerrero, Mago o Arquero); sus atributos de juego quedan fuera de alcance.
- Se asume que el reloj del sistema es la única fuente de tiempo para vigencias y bloqueos.
