# Verificación — 10 de noviembre de 2026

Hardware: OUYA con Android 4.1.2/API 16. Las pruebas utilizaron vídeos públicos de Blender.

- Aplicación original: selección combinada itag 18, 640×360. Cambiar solamente la calidad solicitada no habilitó HD.
- Identificación actualizada: se habilitaron formatos adaptativos; Opus itag 251 dejaba la posición en cero.
- Con Opus deshabilitado: AAC itag 140 y H.264 funcionaron; Sintel se reprodujo con la opción 1080p, imagen panorámica 1920×818.
- Ruta HFR: se habilitó Big Buck Bunny con itag 299, 1920×1080, fuente 60 fps.
- APK HD60 independiente: muestra con Aeropex apagados, A2DP desconectado y mando HID conectado. En 60,703 segundos de reloj el vídeo avanzó 60,696443 segundos. El contador pasó de 3316 a 6964 fotogramas, con cero descartes reportados y sin errores de vídeo en las muestras.
- Se observaron dos paros breves fuera de la fase medida y cortes de audio con Bluetooth. Una fase fluida no prueba estabilidad continua. Los contadores antiguos no son una auditoría exhaustiva de todos los cuadros presentados.

No se verificó audio por otra salida: no estaba disponible para el usuario. No se afirma haber corregido Bluetooth, firmware o controladores. No se probó toda la biblioteca ni reproducción prolongada.

Vídeos utilizados:
- Big Buck Bunny, Blender: https://www.youtube.com/watch?v=aqz-KE-bpKQ
- Sintel, Blender: https://www.youtube.com/watch?v=eRsGyueVLvQ
