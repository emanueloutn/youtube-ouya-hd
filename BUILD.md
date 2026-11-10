# Reconstruir el parche

Requiere Python 3 y una copia de la APK original cuyo SHA-256 sea:

`1a91a635aa8e769e86d683dcbff86e1508b7f7d6f2fb308f17666bcdf43b671b`

No se incluye esa APK original en el repositorio. Usa tu propio respaldo.

```powershell
python tools/patch_youtube_hd60.py --input YouTube-OUYA-original.apk --output build
```

La salida es `build/youtube-hd60-unsigned.apk`. El script usa solo la biblioteca estándar. Verifica la huella de entrada, conserva la distribución de las cadenas DEX, recalcula sus sumas de comprobación y cambia únicamente manifiesto y DEX. La biblioteca nativa queda intacta.

Para instalar el resultado debes alinearlo con `zipalign` y firmarlo con `apksigner` del Android SDK. Para Android 4.1 activa firma v1. Genera y conserva tu propia clave de desarrollo; no uses claves de otras personas. No se publica la clave de la APK de prueba.

La APK publicada usa una firma de prueba comunitaria y un paquete distinto del original. Una reconstrucción con otra clave no puede actualizar directamente una instalación firmada con la clave de la publicación.
