# YouTube OUYA HD60 — experimental

Parche comunitario **no oficial** para la aplicación antigua de YouTube de OUYA con Android 4.1. Habilita opciones H.264/AAC hasta **1080p60 cuando el vídeo y el reproductor lo permiten**. No está afiliado a Google, YouTube, Sony ni OUYA.

> **Estado alfa:** se ha comprobado reproducción real, pero se observaron dos paros breves y cortes de audio intermitentes. No se garantiza fluidez constante ni compatibilidad con todos los vídeos. Lee [KNOWN-ISSUES.md](KNOWN-ISSUES.md).

## Descargar e instalar

Descarga **YouTube-OUYA-HD60-experimental.apk** desde [Releases](https://github.com/emanueloutn/youtube-ouya-hd/releases).

1. Transfiere la APK a la OUYA e instálala.
2. Abre **YouTube OUYA HD60**. Se instala como una aplicación separada; conserva YouTube original.
3. Selecciona invitado o inicia sesión si lo deseas. La copia no incluye las cuentas de la aplicación original.
4. Reproduce un vídeo y abre Ajustes → Calidad. Selecciona 1080p cuando esté disponible.

No necesita una computadora encendida ni conexión USB para funcionar. Comprueba la descarga con `SHA256SUMS`.

## Cambios

- Identificación de navegador compatible con la reproducción adaptativa del sitio.
- Audio AAC: se deshabilita Opus, que en las pruebas dejaba la reproducción detenida.
- Ruta de compatibilidad HFR para que el reproductor no excluya automáticamente formatos de más de 32 fps.
- Nombre, paquete y permiso de sandbox separados para conservar la instalación original.

La identificación de compatibilidad incluye `PS4; Leanback Shell`: el sitio o la cuenta pueden mostrar PlayStation 4. **El hardware y el motor antiguo no se actualizan**. No se modifican DRM, compras ni controles de acceso. No se añaden funciones propias para omitir anuncios.

## Verificación

Prueba en una OUYA real con Big Buck Bunny, vídeo H.264 itag 299 de **1920×1080 a 60 fps**, audio AAC itag 140. En una ventana de 60,703 segundos la posición avanzó 60,696 segundos y el contador registró 3648 fotogramas adicionales, aproximadamente 60 por segundo, sin descartes reportados. Estos contadores no garantizan cada cuadro presentado físicamente en pantalla.

El usuario observó dos paros breves en otra fase y cortes de audio intermitentes. El Bluetooth es una hipótesis pendiente, no una causa confirmada. [Resultados y límites](VERIFICATION.md).

## Código del parche

`tools/patch_youtube_hd60.py` modifica una APK original concreta y produce una APK **sin firmar**. El código completo de YouTube/Chromium no forma parte de este repositorio.

```powershell
python tools/patch_youtube_hd60.py --input YouTube-OUYA-original.apk --output build
```

Consulta [BUILD.md](BUILD.md) para alinear y firmar el resultado con tu propia clave. No se publican claves de firma, cuentas, cookies ni registros privados de la consola.

## Apoyar el mantenimiento

El apoyo es voluntario y no desbloquea funciones ni representa un pago a YouTube.

- [Apoyar en Ko-fi](https://ko-fi.com/enmanuelyepez)
- [Apoyar en PayPal](https://paypal.me/EnmanuelFYepez)

También puedes ayudar reportando fallos con resolución, frecuencia de cuadros, conexión y salida de audio. No incluyas contraseñas, cookies ni URLs firmadas de vídeo.

## Derechos y componentes

Es una modificación experimental de software de terceros, no una aplicación original escrita desde cero. Las marcas y componentes pertenecen a sus respectivos titulares y mantienen sus condiciones; no se ofrece una licencia MIT sobre la APK completa. Consulta [NOTICE.md](NOTICE.md).

English: unofficial experimental compatibility patch for the legacy OUYA YouTube app. Enables compatible H.264/AAC playback up to 1080p60. Intermittent stalls and audio interruptions remain under investigation. See the release notes before installing.
