# Weatherware
Sometimes you look outside, and it's sunny, so you dress according to the sun, but once you go outside, it's really cold, and you regret not bringing a jacket, or
in the opposite case its really cold when you leave the house, and a couple of hours later, you find yourself sweating because the temperature changed so quickly. 
Weatherware is the solution for that. You just use Weatherware on your computer, and it suggests to you what to wear for the day and to dress accordingly, in some cases
it even gives you a UV warning to remind you to wear sunscreen and take care of your skin. Weatherware is a convenient way to easily choose what to wear and feel comfortable
for the whole day without having to think about it or spend time planning what to wear. 

## Installation
```bash
pip install uv
```
```bash
uv add "git+https://github.com/mpkcb21/weatherware.git"
```
or 
```
uv tool install "git+https://github.com/mpkcb21/weatherware.git"
```

## Usage

```bash
weatherware 
```

Basic usage:
```bash
weatherware "San Diego"
weatherware "Rancho Cucamonga"
weatherware San Diego
weatherware Rancho Cucamonga
```

If you run cold, use `--cold-bias` to shift recommendations warmer (shifts the recommendation by 5 degrees):
```bash
weatherware "San Francisco" --cold-bias
```

Show full weather stats alongside the recommendation:
```bash
weatherware "Boston" --raw
```

## Example Output

```
  📍 Rancho Cucamonga, California, United States
  Clear sky · 84°F (feels like 86°F)

  ☀️  UV index 9 (very high) — apply sunscreen even if it doesn't feel hot.
  🌡️  Big temp swing today (54°F → 86°F feels-like) — dress in layers you can remove.

  What to wear:
  Top:           lightweight t-shirt or tank top
  Bottom:        shorts or a light skirt
  Outer layer:   none
  Accessories:   sunglasses, sunscreen (SPF 30+), hat for sun protection
```
raw example:

```
  📍 Rancho Cucamonga, California, United States
  Clear sky · 84°F (feels like 86°F)

  ☀️  UV index 9 (very high) — apply sunscreen even if it doesn't feel hot.
  🌡️  Big temp swing today (54°F → 86°F feels-like) — dress in layers you can remove.

  What to wear:
  Top:           lightweight t-shirt or tank top
  Bottom:        shorts or a light skirt
  Outer layer:   none
  Accessories:   sunglasses, sunscreen (SPF 30+), hat for sun protection

  Weather details:
  Wind:          8 mph (gusts 10 mph)
  Humidity:      33%
  UV index:      9
  Rain chance:   0% (today's max)
  Day range:     54°F – 86°F feels-like
```

