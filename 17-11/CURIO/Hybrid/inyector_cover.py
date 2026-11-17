import os
from mutagen.id3 import ID3, APIC, error
from mutagen.mp3 import MP3

def incrustar_caratula(carpeta_musica, nombre_imagen="cover"):
    # Buscar la extensión de la imagen (puede ser .jpg, .jpeg o .png)
    imagen_path = None
    for ext in [".jpg", ".jpeg", ".png"]:
        possible_path = os.path.join(carpeta_musica, f"{nombre_imagen}{ext}")
        if os.path.exists(possible_path):
            imagen_path = possible_path
            break

    if not imagen_path:
        print(f"Error: No se encontró ninguna imagen '{nombre_imagen}.jpg', '.jpeg' o '.png' en la carpeta.")
        return

    # Determinar el tipo MIME según la extensión
    if imagen_path.lower().endswith(".png"):
        mime_type = "image/png"
    else:
        mime_type = "image/jpeg"

    # Leer los datos de la imagen una sola vez
    with open(imagen_path, "rb") as f:
        imagen_data = f.read()

    print(f"Usando la imagen: {os.path.basename(imagen_path)}")

    # Recorrer la carpeta buscando archivos MP3
    archivos_mp3 = [f for f in os.listdir(carpeta_musica) if f.lower().endswith(".mp3")]
    
    if not archivos_mp3:
        print("No se encontraron archivos MP3 en la carpeta especificada.")
        return

    for archivo in archivos_mp3:
        ruta_mp3 = os.path.join(carpeta_musica, archivo)
        try:
            audio = MP3(ruta_mp3, ID3=ID3)
            
            # Si el archivo no tiene etiquetas ID3, se las creamos
            if audio.tags is None:
                audio.add_tags()

            # Eliminar carátulas anteriores para evitar duplicados (opcional)
            audio.tags.delall("APIC")

            # Añadir la nueva carátula
            audio.tags.add(
                APIC(
                    encoding=3,         # 3 para utf-8
                    mime=mime_type,     # 'image/jpeg' o 'image/png'
                    type=3,             # 3 es para 'Cover (front)' / Portada frontal
                    desc='Cover',
                    data=imagen_data
                )
            )
            
            audio.save()
            print(f"[OK] Carátula añadida a: {archivo}")
        except Exception as e:
            print(f"[ERROR] No se pudo procesar {archivo}: {e}")

if __name__ == "__main__":
    # Cambia esto por la ruta de tu carpeta de música (o usa "." si el script está dentro de la misma carpeta)
    # Ejemplo en Windows: r"C:\Users\TuUsuario\Musica"
    # Ejemplo en Linux/Mac: "/home/usuario/Musica"
    ruta_carpeta = "." 
    
    incrustar_caratula(ruta_carpeta, nombre_imagen="cover")