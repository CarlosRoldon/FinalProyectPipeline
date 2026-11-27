# Módulo: Cuentas de jugador y sesión

## 1. Contexto y alcance

El RPG Manager es un sistema de consola para administrar personajes de rol. Este módulo permite que una persona se registre con una cuenta, inicie y cierre sesión, recupere su contraseña y asocie personajes a su cuenta. Queda fuera de alcance la creación, edición y eliminación de personajes (de eso se ocupa otro módulo), la eliminación de cuentas, el envío real de correos electrónicos, la autenticación de dos factores y el inicio de sesión con redes sociales. Este módulo define su propia versión mínima de Personaje, con solo nombre y clase.

## 2. Actores

- **Visitante**: persona que no tiene una sesión activa, tenga o no una cuenta registrada; se registra, inicia sesión o recupera su contraseña.
- **Jugador**: persona con una sesión activa; consulta su perfil y administra los personajes de su cuenta.
- **Sistema**: temporizador interno del módulo que aplica los vencimientos de sesiones y bloqueos sin intervención de una persona.

## 3. Requerimientos funcionales

- **RF-01** El visitante puede registrar una cuenta indicando nombre de usuario, correo electrónico y contraseña.
  - Criterio de aceptación: con datos que cumplen RN-01, RN-02 y RN-03, el sistema crea la cuenta en estado Activa, con 0 personajes, 0 intentos fallidos y sin fecha de bloqueo; si algún dato incumple una regla, no se crea la cuenta y el mensaje indica la regla violada.
- **RF-02** El visitante con cuenta registrada puede iniciar sesión con su nombre de usuario y su contraseña; al iniciar sesión pasa a ser jugador.
  - Criterio de aceptación: con credenciales correctas y cuenta en estado Activa, el sistema crea una sesión en estado Activa asociada a la cuenta y pone en 0 el contador de intentos fallidos; con credenciales incorrectas no crea sesión, el contador aumenta en 1 y, si llega a 5, se aplica RN-04; con la cuenta en estado Bloqueada no crea sesión aunque las credenciales sean correctas.
- **RF-03** El jugador puede cerrar su sesión.
  - Criterio de aceptación: tras cerrar la sesión, su estado es Cerrada y cualquier consulta de perfil o de personajes con esa sesión es rechazada.
- **RF-04** El jugador puede consultar su perfil.
  - Criterio de aceptación: el perfil muestra nombre de usuario, correo, fecha de registro y cantidad de personajes de la cuenta; no muestra la contraseña.
- **RF-05** El visitante puede solicitar la recuperación de su contraseña indicando su correo electrónico.
  - Criterio de aceptación: si el correo pertenece a una cuenta, el sistema busca la cuenta por su correo y genera un token de recuperación que cumple RN-07; la respuesta al visitante es la misma exista o no el correo, según RN-08.
- **RF-06** El visitante puede restablecer su contraseña presentando un token de recuperación y una contraseña nueva.
  - Criterio de aceptación: el sistema ejecuta estos pasos en orden: 1) verifica que el token está vigente y no usado según RN-07; 2) verifica que la contraseña nueva cumple RN-02; 3) cambia la contraseña de la cuenta; 4) marca el token como usado; 5) pone en 0 el contador de intentos fallidos y deja la cuenta en estado Activa; 6) cierra las sesiones activas de la cuenta. Si falla el paso 1 o el paso 2, no se ejecuta ningún paso posterior y no cambia nada.
- **RF-07** El jugador puede asociar un personaje a su cuenta indicando el nombre y la clase del personaje.
  - Criterio de aceptación: si el nombre cumple RN-10, la clase cumple RN-11 y la cuenta tiene menos personajes que el máximo de RN-05, la cantidad de personajes de la cuenta aumenta en 1 y el personaje aparece en su lista; en cualquier otro caso, el sistema rechaza la asociación, indica la regla violada y no cambia la lista.
- **RF-08** El jugador puede listar los personajes de su cuenta.
  - Criterio de aceptación: la lista muestra el nombre y la clase de cada personaje asociado a su cuenta y ningún personaje de otra cuenta.
- **RF-09** El sistema cierra automáticamente las sesiones inactivas.
  - Criterio de aceptación: una sesión en estado Activa cuyo último movimiento ocurrió hace 30 minutos o más pasa a estado Cerrada, según RN-09.
- **RF-10** El sistema desbloquea automáticamente las cuentas bloqueadas.
  - Criterio de aceptación: una cuenta en estado Bloqueada cuya fecha de bloqueo fue hace 15 minutos o más pasa a estado Activa con 0 intentos fallidos, según RN-04.

## 4. Requerimientos no funcionales

- **RNF-01** Las contraseñas se guardan solo como hash con sal, con un costo de al menos 10 en bcrypt; ninguna contraseña se guarda en texto plano. Se verifica con una prueba automática sobre el almacenamiento, no con un diagrama.
- **RNF-02** El inicio de sesión responde en menos de 2 segundos con hasta 10000 cuentas registradas. Se verifica con una prueba de rendimiento, no con un diagrama.
- **RNF-03** Las reglas de negocio de este módulo tienen pruebas unitarias con al menos 70 % de cobertura.
- **RNF-04** El 100 % de los mensajes de error en español indica el código de la regla de negocio violada (por ejemplo, RN-01).

## 5. Reglas de negocio

- **RN-01** El nombre de usuario es único sin distinguir mayúsculas de minúsculas, tiene entre 4 y 20 caracteres y solo contiene letras y dígitos.
- **RN-02** La contraseña tiene al menos 8 caracteres, con al menos una mayúscula, una minúscula y un dígito, y no puede ser igual al nombre de usuario.
- **RN-03** El correo electrónico es único en el sistema y tiene el formato texto@dominio.
- **RN-04** Cuando el contador de intentos fallidos consecutivos llega a 5, la cuenta pasa a estado Bloqueada y se guarda la fecha de bloqueo; la cuenta permanece Bloqueada durante 15 minutos desde esa fecha, y mientras está Bloqueada no se puede iniciar sesión aunque la contraseña sea correcta.
- **RN-05** Una cuenta puede tener entre 0 y 3 personajes asociados; no se puede asociar un cuarto personaje.
- **RN-06** Un personaje pertenece a una sola cuenta.
- **RN-07** Un token de recuperación es válido durante 30 minutos desde su creación y se puede usar una sola vez; al generar un token nuevo para una cuenta, el anterior deja de ser válido.
- **RN-08** Los mensajes del sistema no revelan si el nombre de usuario o el correo existen: ante credenciales inválidas se muestra el mismo mensaje sin importar cuál dato falló.
- **RN-09** Una sesión sin actividad durante 30 minutos pasa a estado Cerrada.
- **RN-10** El nombre de un personaje es único dentro de su cuenta, sin distinguir mayúsculas de minúsculas, y tiene entre 3 y 20 caracteres; dos cuentas distintas pueden tener personajes con el mismo nombre.
- **RN-11** La clase de un personaje es exactamente una de estas tres: Guerrero, Mago o Arquero.

## 6. Supuestos y glosario

- **Cuenta**: registro de un jugador con nombre de usuario (que la identifica), correo, contraseña (como hash), estado (Activa o Bloqueada), contador de intentos fallidos, fecha de bloqueo (vacía si no está bloqueada) y fecha de registro.
- **Sesión**: periodo en que una persona está autenticada; tiene un identificador propio, un estado (Activa o Cerrada) y una fecha de último movimiento; pertenece a una sola cuenta.
- **Intento fallido consecutivo**: inicio de sesión con credenciales incorrectas sin ningún inicio correcto en medio.
- **Token de recuperación**: código de un solo uso, con fecha de creación y estado (usado o no usado), que permite restablecer la contraseña y pertenece a una sola cuenta. Se asume que el sistema lo muestra en consola en lugar de enviarlo por correo.
- **Personaje**: en este módulo, solo un nombre y una clase (Guerrero, Mago o Arquero); se identifica por su cuenta y su nombre; sus atributos de juego quedan fuera de alcance.
- **Relación Cuenta–Personaje**: la cuenta agrupa a sus personajes (de 0 a 3, según RN-05); el personaje se crea fuera de este módulo y no se elimina al cerrar una sesión.
- Se asume que el reloj del sistema es la única fuente de tiempo para vigencias y bloqueos.
