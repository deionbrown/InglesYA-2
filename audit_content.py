
from curriculum import LEVELS,CURRICULUM,lesson
from content_engine import build_pack
errors=[]; count=0
for level in LEVELS:
    for unit in range(1,11):
        for letter in "ABCD":
            d=lesson(level,unit,letter)
            p=build_pack(level,unit,letter,d["title"])
            count+=1
            required=["vocabulary","examples","grammar_note","dialogue","reading","exercises","evaluation","homework","grammar","pron","goal"]
            for k in required:
                if not p.get(k): errors.append((level,unit,letter,k))
            if len(p["vocabulary"])<15: errors.append((level,unit,letter,"vocab<15"))
            if len(p["evaluation"])<5: errors.append((level,unit,letter,"eval<5"))
print("LESSONS",count)
print("ERRORS",len(errors))
if errors: print(errors[:30])
