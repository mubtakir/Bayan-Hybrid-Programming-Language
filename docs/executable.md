# بناء وتشغيل برامج بيان كملفات تنفيذية

هذا الدليل يشرح طرقًا عملية لجعل برنامج بيان (.bayan) قابلاً للتشغيل كأنه ملف تنفيذي على لينكس/ويندوز/ماك.

الفكرة العامة: بيان تعمل عبر مفسر مكتوب ببايثون. لذا نوفّر "مشغِّل" Python صغير يقرأ ملف .bayan ويمرره إلى مفسر بيان، ثم نغلف هذا المشغل بطرق مختلفة (صلاحيات تنفيذ، PyInstaller، zipapp) ليصبح تطبيقًا تنفيذيًا.

## 1) تشغيل مباشر عبر مشغِّل عام (موصى به للبداية)
- وفّرنا سكربت عام:
  - scripts/bayan_run.py
- الاستعمال:
  - Linux/macOS:
    - python3 scripts/bayan_run.py path/to/app.bayan
  - Windows (PowerShell):
    - py scripts/bayan_run.py path\to\app.bayan
- خيارات مفيدة:
  - --colors لتمكين التلوين
  - --context=N لعدد أسطر السياق في code frames
  - --tabstop=4 لضبط عرض التبويبات

## 2) جعل التشغيل بنقرة (chmod +x + shebang)
- على Linux/macOS:
  1) اجعل المشغِّل قابلاً للتنفيذ:
     - chmod +x scripts/bayan_run.py
  2) يمكنك إنشاء ملف شِل صغير "bayan" يلتقط المسار ويمرره:
     - أنشئ bin/bayan بمحتوى:
       - #!/usr/bin/env bash
       - python3 "$(dirname "$0")/../scripts/bayan_run.py" "$@"
     - ثم chmod +x bin/bayan
  3) أضف bin/ إلى PATH لديك أو نفّذ مباشرة: bin/bayan myprog.bayan

## 3) إنشاء ملف تنفيذي أصلي ببايثون (PyInstaller)
- يتيح PyInstaller توليد ملف تنفيذي واحد يجمع مفسر بيان مع المشغِّل.
- خطوات (على بيئتك):
  1) تثبيت الأداة:
     - pip install pyinstaller
  2) توليد التنفيذية:
     - pyinstaller --onefile scripts/bayan_run.py --name bayan-run
  3) التشغيل:
     - dist/bayan-run path/to/app.bayan
- ملاحظات:
  - هذا يدمج مفسر بيان داخل التنفيذية.
  - تأكد من أن بايثون/الحزم في نفس البيئة.

## 4) حزمة zipapp (بدون تبعيات خارجية)
- zipapp مدمجة في بايثون لإنشاء أرشيف قابل للتشغيل.
- الفكرة: إعداد نقطة دخول __main__.py تستدعي bayan_run ثم إنشاء zipapp.
- مثال مختصر:
  1) أنشئ مجلد app_runner/ يحوي ملف __main__.py يستورد دالة التشغيل من scripts/bayan_run.py
  2) نفّذ:
     - python3 -m zipapp app_runner -m "__main__:main" -o bayan_run.pyz
  3) التشغيل:
     - python3 bayan_run.pyz path/to/app.bayan

## 5) طريقة "تغليف التطبيق" مع بياناته
- إن أردت تطبيقًا مستقلًا بملفه .bayan المضمن:
  1) اكتب مشغِّل Python صغيرًا يحمّل نص برنامجك من ملف مضمن (أو كـ resource) بدل قراءة ملف خارجي.
  2) استخدم PyInstaller --onefile على هذا المشغِّل الخاص.
  3) هكذا تحصل على app.exe (ويندوز) أو app (لينكس/ماك) يعمل مباشرة.

## 6) ملاحظات منصات التشغيل
- Linux/macOS:
  - shebang + chmod +x يمنح تجربة تنفيذ مباشرة.
  - PyInstaller يخرج ملفًا تنفيذيًا عادة بدون تبعيات.
- Windows:
  - استخدم py scripts/bayan_run.py أو PyInstaller لإنتاج app.exe.

## 7) أحسن ممارسات
- احتفظ ببرامج البيان داخل مجلد src/ أو apps/ ونفّذها عبر scripts/bayan_run.py.
- أضف اختباراتك واستعمل pytest للتأكد.
- عند إنشاء تنفيذية، اختبر على نفس المنصة التي سيعمل عليها المستخدم النهائي.

انتهى.

