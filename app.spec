import logging
import os
import sys

import webview

from neura.predictor import Predictor

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger("neura")

DEFAULTS = {
    "company": "Dell", "typename": "Notebook", "ram": 16, "weight": 1.0,
    "touchscreen": 0, "ips": 1, "ppi": 141, "cpubrand": "Intel Core i5",
    "hdd": 0, "ssd": 512, "gpubrand": "Intel (Integrated)", "os": "Windows",
}


def resource_path(relative_path: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, relative_path)


class Api:
    def __init__(self):
        # underscore, чтобы pywebview не пытался разбирать объект модели
        self._predictor = Predictor(resource_path("models/model.pkl"))

    def compute_price(self, specs: dict) -> dict:
        try:
            s = {**DEFAULTS, **{k: v for k, v in specs.items() if v not in (None, "")}}
            laptop = {
                "Company": s["company"],
                "TypeName": s["typename"],
                "Ram": float(s["ram"]),
                "Weight": float(s["weight"]),
                "TouchScreen": int(s["touchscreen"]),
                "Ips": int(s["ips"]),
                "Ppi": float(s["ppi"]),
                "Cpu_brand": s["cpubrand"],
                "HDD": float(s["hdd"]),
                "SSD": float(s["ssd"]),
                "Gpu_brand": s["gpubrand"],
                "Os": s["os"],
            }
            return {"success": True, **self._predictor.predict(laptop)}
        except (ValueError, KeyError, TypeError) as e:
            log.warning("Некорректные входные данные: %s", e)
            return {"success": False, "error": "Проверь введённые характеристики"}
        except Exception:
            log.exception("Ошибка расчёта")
            return {"success": False, "error": "Внутренняя ошибка"}


def main():
    webview.create_window(
        title="NEURA-PRICE // AI — Laptop Evaluator",
        url=resource_path("assets/style.html"),
        width=1280, height=850, resizable=True,
        background_color="#0b0f19",
        js_api=Api(),
    )
    webview.start(debug=False)


if __name__ == "__main__":
    main()