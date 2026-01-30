import os
root = "dataset/train"
for cls in sorted(os.listdir(root)):
    cls_path = os.path.join(root, cls)
    if os.path.isdir(cls_path):
        count = len([f for f in os.listdir(cls_path) if f.lower().endswith(('.jpg','.png','.jpeg'))])
        print(f"{cls}: {count} images")
