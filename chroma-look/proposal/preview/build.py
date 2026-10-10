import base64, json, os, sys
S = os.path.dirname(os.path.abspath(__file__)) + "/.."
A = S + "/assets/"
uri = lambda f, t="image/webp": f"data:{t};base64," + base64.b64encode(open(A + f, "rb").read()).decode()
L = {}
L["feast"] = json.load(open(S + "/lights/feast.json"))["a feast in a year of trust"]
love = json.load(open(S + "/lights/ink.json"))["falling in love"]
for l in love:
    if l["x"] > 760 and l["y"] < 120: l["cold"] = True
L["love"] = love
s = open(S + "/preview/src.html", encoding="utf-8").read()
sub = {"{{SPRITE}}": open(A + "sprite.svg", encoding="utf-8").read(), "{{FEAST}}": uri("a-feast-in-a-year-of-trust.webp"), "{{LOVE}}": uri("falling-in-love.webp"),
       "{{BEFORE_MOMENT}}": uri("4-moment-1280.webp"), "{{BEFORE_OUT}}": uri("7-outcome-1280.webp"),
       "{{CHILD}}": uri("child.webp"), "{{YOUTH}}": uri("youth.webp"), "{{ADULT}}": uri("adult.webp"), "{{ELDER}}": uri("elder.webp"),
       "{{LIGHTS}}": json.dumps(L, separators=(",", ":"))}
for k, v in sub.items():
    assert k in s, k
    s = s.replace(k, v)
open(S + "/preview/chroma-ink-look.html", "w", encoding="utf-8").write(s)
print("built", len(s))
