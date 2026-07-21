import sys

with open("frontend/app/page.tsx", "r") as f:
    lines = f.readlines()

out = []
skip = False
for line in lines:
    if line.startswith("function AssessmentView("):
        skip = True
    if line.startswith("export default function Home"):
        skip = False
    
    if not skip:
        out.append(line)

with open("frontend/app/page.tsx", "w") as f:
    f.writelines(out)
