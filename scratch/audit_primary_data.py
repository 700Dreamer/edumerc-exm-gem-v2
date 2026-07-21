import os

db_path = "/Users/luke/Downloads/docs/ eduquest 2 stabler/EduQuest_Syllabus_Database/2. Primary"
classes = [
    "P1_Lower_Primary", "P2_Lower_Primary", "P3_Lower_Primary",
    "P4_Upper_Primary", "P5_Upper_Primary", "P6_Upper_Primary", "P7_Upper_Primary"
]

print("=== EDUQUEST DATABASE DATA AUDIT ===")
print("Checking for required data for EDUMERC policy...\n")

total_missing = 0

for cls in classes:
    cls_path = os.path.join(db_path, cls)
    if not os.path.exists(cls_path):
        print(f"❌ {cls}: DIRECTORY MISSING COMPLETELY!")
        total_missing += 1
        continue
        
    print(f"✅ {cls}:")
    
    # Count files in subjects
    subjects = os.listdir(cls_path)
    file_count = 0
    subj_counts = {}
    for subj in subjects:
        subj_path = os.path.join(cls_path, subj)
        if os.path.isdir(subj_path):
            files = [f for f in os.listdir(subj_path) if not f.startswith('.')]
            subj_counts[subj] = len(files)
            file_count += len(files)
            
    if file_count == 0:
        print(f"   -> ❌ NO FILES FOUND in any subject!")
        total_missing += 1
    else:
        for subj, count in subj_counts.items():
            print(f"   -> {subj}: {count} files")

print(f"\nAudit complete. Missing or empty classes: {total_missing}")
