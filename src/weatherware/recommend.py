"""Map weather conditions to outfit recommendations."""

from dataclasses import dataclass, field


@dataclass
class Outfit:
    top: str
    bottom: str
    outer: str
    accessories: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def recommend(weather: dict, cold_bias: bool = False) -> Outfit:
    """
    Generate an outfit recommendation from a weather dict.
    cold_bias: user runs cold — shift thresholds warmer by ~5°F.
    """
    feels = weather["feels_like_f"]
    actual = weather["temp_f"]
    wind = weather["wind_mph"]
    gusts = weather["wind_gusts_mph"]
    humidity = weather["humidity_pct"]
    uv = weather["uv_index"]
    precip_prob = weather["max_precip_prob_pct"]
    code = weather["weather_code"]
    day_min = weather["day_feels_min_f"]
    day_max = weather["day_feels_max_f"]

    bias = 5 if cold_bias else 0
    effective = feels - bias

    warnings = []

    # --- Deceptive weather detection ---
    temp_feels_gap = actual - feels
    if temp_feels_gap >= 8:
        warnings.append(
            f"⚠️  Deceptive: actual {actual:.0f}°F but feels like {feels:.0f}°F "
            f"(wind chill of {temp_feels_gap:.0f}°F) — dress warmer than it looks."
        )

    if wind >= 20:
        warnings.append(f"💨 Windy ({wind:.0f} mph, gusts up to {gusts:.0f} mph) — avoid loose layers.")

    if humidity >= 80 and effective >= 75:
        warnings.append(f"💧 High humidity ({humidity:.0f}%) — will feel hotter and stickier than the temp suggests.")

    if uv >= 6 and weather.get("is_day", 1):
        level = "very high" if uv >= 8 else "high"
        warnings.append(f"☀️  UV index {uv:.0f} ({level}) — apply sunscreen even if it doesn't feel hot.")

    day_swing = day_max - day_min
    if day_swing >= 20:
        warnings.append(
            f"🌡️  Big temp swing today ({day_min:.0f}°F → {day_max:.0f}°F feels-like) — "
            "dress in layers you can remove."
        )

    is_raining = code in {51, 53, 55, 61, 63, 65, 80, 81, 82}
    is_snowing = code in {71, 73, 75, 77, 85, 86}
    is_stormy = code in {95, 96, 99}

    accessories = []

    # --- Rain / snow / storm ---
    if is_stormy or is_raining or precip_prob >= 60:
        accessories.append("umbrella or rain jacket")
    elif precip_prob >= 35:
        accessories.append("umbrella (just in case)")

    if is_snowing:
        accessories.append("waterproof boots")

    # --- UV / sun ---
    if uv >= 3 and weather.get("is_day", 1):
        accessories.append("sunglasses")
    if uv >= 6 and weather.get("is_day", 1):
        accessories.append("sunscreen (SPF 30+)")
    if uv >= 8 and weather.get("is_day", 1):
        accessories.append("hat for sun protection")

    # --- Outfit by feels-like temp ---
    if effective >= 85:
        top = "lightweight t-shirt or tank top"
        bottom = "shorts or a light skirt"
        outer = "none"
    elif effective >= 75:
        top = "t-shirt"
        bottom = "shorts or light pants"
        outer = "none"
        if humidity >= 70:
            top = "breathable t-shirt (moisture-wicking recommended)"
    elif effective >= 65:
        top = "light t-shirt or polo"
        bottom = "jeans or chinos"
        outer = "light cardigan or zip-up (optional)"
    elif effective >= 55:
        top = "long-sleeve shirt or light sweater"
        bottom = "jeans or trousers"
        outer = "light jacket"
    elif effective >= 45:
        top = "sweater or fleece"
        bottom = "jeans or heavier trousers"
        outer = "medium jacket or hoodie"
    elif effective >= 35:
        top = "thermal or heavy sweater"
        bottom = "lined pants or thick jeans"
        outer = "heavy jacket or coat"
        accessories.append("gloves")
        accessories.append("scarf")
    elif effective >= 20:
        top = "thermal base layer + sweater"
        bottom = "thermal leggings under pants"
        outer = "heavy insulated coat"
        accessories.extend(["gloves", "scarf", "warm hat"])
    else:
        top = "thermal base layer + heavy sweater"
        bottom = "thermal leggings under thick pants"
        outer = "heavy insulated coat (face coverage recommended)"
        accessories.extend(["insulated gloves", "scarf", "warm hat", "hand warmers"])
        warnings.append("🥶 Dangerously cold — minimize time outdoors and cover all exposed skin.")

    # Wind adjustment to outer layer
    if wind >= 15 and outer == "none":
        outer = "light windbreaker (wind is noticeable)"
    elif wind >= 25 and "jacket" in outer and "heavy" not in outer:
        outer = outer.replace("jacket", "jacket (zip up fully — it's windy)")

    return Outfit(
        top=top,
        bottom=bottom,
        outer=outer,
        accessories=list(dict.fromkeys(accessories)),
        warnings=warnings,
    )