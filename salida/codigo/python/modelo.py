"""Esqueleto generado por spec2code. Módulo: Cuentas de jugador y sesión

NO es una solución: son clases y firmas con TODO. Completa la lógica, audita cada
clase contra la spec y corrige la SPEC (no este archivo) cuando el error venga de ella.
"""
from __future__ import annotations

from datetime import date


class Cuenta:
    """Cuenta. Trazabilidad: RF-01, RF-02, RF-04, RF-05, RF-06, RF-10, RN-01, RN-03, RN-04, RN-05."""

    def __init__(self, nombre_usuario: str, correo: str, contrasena_hash: str, estado: str, intentos_fallidos: int, fecha_bloqueo: date, fecha_registro: date) -> None:
        self.nombre_usuario: str = nombre_usuario  # TODO: encapsulamiento (propiedades)
        self.correo: str = correo  # TODO: encapsulamiento (propiedades)
        self.contrasena_hash: str = contrasena_hash  # TODO: encapsulamiento (propiedades)
        self.estado: str = estado  # TODO: encapsulamiento (propiedades)
        self.intentos_fallidos: int = intentos_fallidos  # TODO: encapsulamiento (propiedades)
        self.fecha_bloqueo: date = fecha_bloqueo  # TODO: encapsulamiento (propiedades)
        self.fecha_registro: date = fecha_registro  # TODO: encapsulamiento (propiedades)
        self.sesions: list[Sesion] = []  # asociacion: inicia (RF-02, RF-03)
        self.token_recuperacions: list[TokenRecuperacion] = []  # asociacion: solicita (RF-05, RF-06)
        self.personajes: list[Personaje] = []  # agregacion: agrupa (máximo 3) (RF-07, RF-08, RN-05, RN-06)

    def registrar(self) -> None:
        """Crea la cuenta Activa con 0 personajes, 0 intentos y sin fecha de bloqueo (RF-01, RN-01, RN-02, RN-03)."""
        raise NotImplementedError("TODO: implementar Cuenta.registrar")

    def iniciar_sesion(self) -> None:
        """Valida credenciales y estado y crea la sesión Activa (RF-02, RN-08)."""
        raise NotImplementedError("TODO: implementar Cuenta.iniciar_sesion")

    def bloquear(self) -> None:
        """Pasa a Bloqueada y guarda la fecha de bloqueo al llegar a 5 intentos fallidos (RF-02, RN-04)."""
        raise NotImplementedError("TODO: implementar Cuenta.bloquear")

    def desbloquear(self) -> None:
        """Pasa a Activa con 0 intentos tras 15 minutos de bloqueo (RF-10, RN-04)."""
        raise NotImplementedError("TODO: implementar Cuenta.desbloquear")

    def buscar_por_correo(self) -> None:
        """Busca la cuenta por su correo para la recuperación (RF-05, RN-08)."""
        raise NotImplementedError("TODO: implementar Cuenta.buscar_por_correo")

    def consultar_perfil(self) -> list:
        """Devuelve usuario, correo, fecha y cantidad de personajes (RF-04)."""
        raise NotImplementedError("TODO: implementar Cuenta.consultar_perfil")

    def restablecer_contrasena(self) -> None:
        """Cambia la contraseña, reinicia intentos, activa la cuenta y cierra sesiones (RF-06, RN-02)."""
        raise NotImplementedError("TODO: implementar Cuenta.restablecer_contrasena")

    def asociar_personaje(self) -> None:
        """Asocia un personaje si hay menos de 3 y el nombre es único en la cuenta (RF-07, RN-05, RN-10)."""
        raise NotImplementedError("TODO: implementar Cuenta.asociar_personaje")

    def listar_personajes(self) -> list:
        """Lista nombre y clase de sus personajes (RF-08)."""
        raise NotImplementedError("TODO: implementar Cuenta.listar_personajes")


class Sesion:
    """Sesion. Trazabilidad: RF-02, RF-03, RF-09, RN-09."""

    def __init__(self, identificador: str, estado: str, fecha_ultimo_movimiento: date) -> None:
        self.identificador: str = identificador  # TODO: encapsulamiento (propiedades)
        self.estado: str = estado  # TODO: encapsulamiento (propiedades)
        self.fecha_ultimo_movimiento: date = fecha_ultimo_movimiento  # TODO: encapsulamiento (propiedades)

    def cerrar(self) -> None:
        """Pasa la sesión a Cerrada (RF-03)."""
        raise NotImplementedError("TODO: implementar Sesion.cerrar")

    def expirar_por_inactividad(self) -> None:
        """Cierra la sesión con 30 minutos o más sin actividad (RF-09, RN-09)."""
        raise NotImplementedError("TODO: implementar Sesion.expirar_por_inactividad")


class TokenRecuperacion:
    """TokenRecuperacion. Trazabilidad: RF-05, RF-06, RN-07."""

    def __init__(self, codigo: str, fecha_creacion: date, usado: bool) -> None:
        self.codigo: str = codigo  # TODO: encapsulamiento (propiedades)
        self.fecha_creacion: date = fecha_creacion  # TODO: encapsulamiento (propiedades)
        self.usado: bool = usado  # TODO: encapsulamiento (propiedades)

    def generar(self) -> None:
        """Crea un token e invalida el anterior de la cuenta (RF-05, RN-07)."""
        raise NotImplementedError("TODO: implementar TokenRecuperacion.generar")

    def esta_vigente(self) -> bool:
        """Vigente si tiene menos de 30 minutos y no fue usado (RF-06, RN-07)."""
        raise NotImplementedError("TODO: implementar TokenRecuperacion.esta_vigente")

    def marcar_usado(self) -> None:
        """Marca el token como usado (RF-06, RN-07)."""
        raise NotImplementedError("TODO: implementar TokenRecuperacion.marcar_usado")


class Personaje:
    """Personaje. Trazabilidad: RF-07, RF-08, RN-06, RN-10, RN-11."""

    def __init__(self, nombre: str, clase: str) -> None:
        self.nombre: str = nombre  # TODO: encapsulamiento (propiedades)
        self.clase: str = clase  # TODO: encapsulamiento (propiedades)

    def validar_clase(self) -> bool:
        """Acepta solo Guerrero, Mago o Arquero (RN-11)."""
        raise NotImplementedError("TODO: implementar Personaje.validar_clase")
