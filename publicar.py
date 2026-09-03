"""Publica el plugin en la web: empaqueta, sube y COMPRUEBA que se lee.

    python publicar.py              # ensaya: empaqueta y no sube nada
    python publicar.py --subir      # sube de verdad
    python publicar.py --verificar  # solo comprueba lo que ya hay publicado

La configuracion y las credenciales van en `publicar.ini`, que esta en el
.gitignore y no se versiona nunca. Hay una plantilla en `publicar.ini.ejemplo`.

Lo importante de este script no es subir dos ficheros: es la comprobacion final.
Un marketplace mal publicado NO da error en Cowork -el plugin aparece en la
lista y simplemente no se instala nunca-, asi que la unica forma de saber si ha
salido bien es pedir lo publicado desde fuera y mirarlo.
"""

from __future__ import annotations

import argparse
import configparser
import hashlib
import json
import sys
import urllib.request
import zipfile
from ftplib import FTP, FTP_TLS
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
PLUGIN = RAIZ / "plugins" / "gesia-auditoria"
CONFIG = RAIZ / "publicar.ini"


def salida_utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass


def leer_config() -> dict:
    if not CONFIG.is_file():
        raise SystemExit(
            "Falta " + CONFIG.name + ". Copia publicar.ini.ejemplo, renombralo y "
            "rellena tus datos. No se versiona: esta en el .gitignore.")
    cp = configparser.ConfigParser()
    cp.read(CONFIG, encoding="utf-8")
    s = cp["web"]
    base = s.get("url_base", "").strip().rstrip("/")
    if not base.startswith("https://"):
        raise SystemExit("url_base tiene que empezar por https:// — Cowork no "
                         "descarga por http.")
    return {
        "url_base": base,
        "host": s.get("host", "").strip(),
        "usuario": s.get("usuario", "").strip(),
        "clave": s.get("clave", ""),
        "ruta_remota": s.get("ruta_remota", "/").strip(),
        "tls": s.getboolean("tls", fallback=True),
    }


def empaquetar() -> tuple:
    """Devuelve (ruta del zip, sha256, version). El plugin va en la RAIZ del zip."""
    man = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    version = man["version"]
    destino = RAIZ / ("gesia-auditoria-" + version + ".zip")

    ficheros = sorted(p for p in PLUGIN.rglob("*")
                      if p.is_file() and "__pycache__" not in p.parts)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for p in ficheros:
            z.write(p, p.relative_to(PLUGIN).as_posix())

    dentro = zipfile.ZipFile(destino).namelist()
    if ".claude-plugin/plugin.json" not in dentro:
        raise SystemExit("el zip no lleva el manifiesto en su raiz")

    digest = hashlib.sha256(destino.read_bytes()).hexdigest()
    print("Empaquetado " + destino.name)
    print("  " + str(len(ficheros)) + " ficheros · "
          + format(destino.stat().st_size / 1e6, ".1f") + " MB")
    print("  sha256 " + digest)
    return destino, digest, version


def escribir_manifiesto(cfg: dict, zip_nombre: str, digest: str) -> Path:
    """El marketplace.json que se publica.

    La url del archivo TIENE que compartir origen con este fichero. Si no, el
    plugin sale en la lista del cliente y no se descarga nunca, sin un mensaje
    de error en ningun sitio. Por eso se construye desde url_base y no se pide
    aparte: asi no pueden discrepar.
    """
    man = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    mkt = {
        "name": "ensys",
        "owner": {"name": "Ensys Consultores Informáticos, S.L."},
        "description": ("Plugins de auditoría de Ensys Consultores para trabajar "
                        "sobre expedientes de Gesia."),
        "plugins": [
            {
                "name": "gesia-auditoria",
                "description": man["description"],
                "author": {"name": "Ensys Consultores Informáticos, S.L."},
                "source": {
                    "source": "archive",
                    "url": cfg["url_base"] + "/" + zip_nombre,
                    "sha256": digest,
                },
            }
        ],
    }
    destino = RAIZ / "marketplace.json"
    destino.write_text(json.dumps(mkt, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")
    print("Escrito marketplace.json  ->  " + mkt["plugins"][0]["source"]["url"])
    return destino


def _asegurar_carpeta(ftp, ruta: str) -> None:
    """Entra en la carpeta remota, creando los tramos que falten.

    La primera vez la carpeta no existe y `cwd` falla con un 550 que no dice
    gran cosa. Se crea tramo a tramo en vez de intentarlo de golpe, porque un
    hosting puede tener creado /www y no lo de dentro.
    """
    for tramo in [x for x in ruta.split("/") if x]:
        try:
            ftp.cwd(tramo)
        except Exception:
            ftp.mkd(tramo)
            ftp.cwd(tramo)
            print("  creada carpeta remota " + tramo)


def subir(cfg: dict, ficheros: list) -> None:
    ftp = FTP_TLS() if cfg["tls"] else FTP()
    ftp.connect(cfg["host"], 21, timeout=60)
    ftp.login(cfg["usuario"], cfg["clave"])
    if cfg["tls"]:
        ftp.prot_p()                     # cifra tambien los datos, no solo el login
    try:
        if cfg["ruta_remota"] not in ("", "/"):
            _asegurar_carpeta(ftp, cfg["ruta_remota"])
        for f in ficheros:
            with f.open("rb") as fh:
                ftp.storbinary("STOR " + f.name, fh, blocksize=1 << 20)
            print("  subido " + f.name)
    finally:
        try:
            ftp.quit()
        except Exception:
            ftp.close()


def verificar(cfg: dict) -> int:
    """Pide lo publicado desde fuera y lo comprueba. Aqui se cazan los fallos."""
    url_man = cfg["url_base"] + "/marketplace.json"
    print("Verificando " + url_man)
    fallos = []

    try:
        with urllib.request.urlopen(url_man, timeout=45) as r:
            crudo = r.read()
            tipo = r.headers.get("Content-Type", "?")
    except Exception as exc:
        print("  NO SE PUEDE LEER: " + str(exc))
        print("  Si es un 403 o te devuelve una pagina de WordPress, la carpeta "
              "no se esta sirviendo como fichero estatico.")
        return 2

    try:
        mkt = json.loads(crudo)
    except ValueError:
        print("  lo que hay ahi NO es JSON (Content-Type: " + tipo + "). "
              "Seguramente WordPress ha servido una pagina.")
        return 2
    print("  manifiesto legible · " + str(len(mkt.get("plugins", []))) + " plugin(s)")

    for p in mkt.get("plugins", []):
        src = p.get("source", {})
        if not isinstance(src, dict) or src.get("source") != "archive":
            fallos.append("el source de " + p["name"] + " no es un archive")
            continue
        # MISMO ORIGEN, que es el requisito que falla en silencio
        origen_man = "/".join(url_man.split("/")[:3])
        origen_zip = "/".join(src["url"].split("/")[:3])
        if origen_man != origen_zip:
            fallos.append("el zip esta en otro origen (" + origen_zip + " frente a "
                          + origen_man + "): apareceria en la lista y NO se "
                          "instalaria nunca")
        try:
            with urllib.request.urlopen(src["url"], timeout=180) as r:
                datos = r.read()
        except Exception as exc:
            fallos.append("no se puede descargar el zip: " + str(exc))
            continue
        real = hashlib.sha256(datos).hexdigest()
        print("  zip descargado · " + format(len(datos) / 1e6, ".1f") + " MB")
        if real != src.get("sha256"):
            fallos.append("el sha256 NO coincide: el manifiesto dice "
                          + str(src.get("sha256"))[:16] + "… y el fichero es "
                          + real[:16] + "…. Claude rechaza el archivo y no "
                          "instala nada.")
        else:
            print("  sha256 coincide")

    for f in fallos:
        print("\n  FALLO: " + f)
    if fallos:
        return 2
    print("\nPublicado y comprobado. Lo que le pasas al cliente es:")
    print("  " + url_man)
    return 0


def main() -> int:
    salida_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--subir", action="store_true", help="sube de verdad")
    p.add_argument("--verificar", action="store_true",
                   help="solo comprueba lo ya publicado")
    args = p.parse_args()

    cfg = leer_config()
    if args.verificar:
        return verificar(cfg)

    zip_path, digest, version = empaquetar()
    man_path = escribir_manifiesto(cfg, zip_path.name, digest)

    if not args.subir:
        print("\nEnsayo: no se ha subido nada. Repite con --subir cuando lo veas bien.")
        return 0

    print("\nSubiendo a " + cfg["host"] + cfg["ruta_remota"])
    subir(cfg, [zip_path, man_path])
    print()
    return verificar(cfg)


if __name__ == "__main__":
    sys.exit(main())
